#!/usr/bin/env python3

import os
import requests
import logging
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from dotenv import load_dotenv

# Automatically load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class TrelloClient:
    def __init__(self, key: str = None, token: str = None, list_id: str = None):
        """
        Initialize the TrelloClient.
        
        Credentials are loaded either from the provided parameters or from environment variables.
        
        Args:
            key (str, optional): Trello API key. Defaults to os.getenv("TRELLO_KEY").
            token (str, optional): Trello API token. Defaults to os.getenv("TRELLO_TOKEN").
            list_id (str, optional): Trello list ID. Defaults to os.getenv("TRELLO_LIST_ID").
        
        Raises:
            ValueError: If any credential is missing.
        """
        self.key = key or os.getenv("TRELLO_KEY")
        self.token = token or os.getenv("TRELLO_TOKEN")
        self.list_id = list_id or os.getenv("TRELLO_LIST_ID")
        
        if not (self.key and self.token and self.list_id):
            raise ValueError("Trello API credentials and list ID must be provided either via parameters or via environment variables.")
        
        self.base_url = "https://api.trello.com/1/cards"
        self.session = self._init_session()
        logger.info("TrelloClient initialized successfully.")

    def _init_session(self) -> requests.Session:
        """
        Initialize a requests.Session with a retry strategy.
        
        Returns:
            requests.Session: A session object configured for retrying failed POST requests.
        """
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        return session

    def create_card(self, name: str, desc: str) -> bool:
        """
        Create a Trello card with the specified name and description.
        
        Args:
            name (str): The title of the card.
            desc (str): The description of the card (e.g., test failure details).
        
        Returns:
            bool: True if the card was created successfully, False otherwise.
        """
        payload = {
            "key": self.key,
            "token": self.token,
            "idList": self.list_id,
            "name": name,
            "desc": desc
        }
        try:
            response = self.session.post(self.base_url, params=payload, timeout=10)
            if response.status_code in (200, 201):
                logger.info("Successfully created Trello card: %s", name)
                return True
            else:
                logger.error("Failed to create Trello card '%s'. Status code: %d; Response: %s",
                             name, response.status_code, response.text)
                return False
        except requests.RequestException as e:
            logger.exception("Exception occurred while creating card '%s': %s", name, e)
            return False
        
    def create_failure_cards(self, failures: list) -> list:
    
        results = []
        for failure in failures:
            # Extract test information from the failure dictionary, using default values if necessary.
            test_name = failure.get("test_name", "Unknown Test")
            error_message = failure.get("error_message", "No error message provided")
            traceback_detail = failure.get("traceback", "No traceback available")
            
            # Construct a user-friendly card title.
            card_title = f"Test Failure: {test_name}"
            
            # Build a detailed and well-formatted card description.
            # We use Markdown syntax for emphasis (e.g., '**' for bold text).
            card_description = (
                f"**Error:** {error_message}\n\n"
                f"**Traceback:**\n{traceback_detail}\n\n"
                "Please review the error details and take corrective measures."
            )
            
            # Attempt to create the Trello card. 
            # The create_card() method already handles HTTP errors and logs them.
            try:
                status = self.create_card(card_title, card_description)
            except Exception as e:
                # Log any unexpected exceptions that occur during card creation.
                logger.error("Exception while creating Trello card for '%s': %s", test_name, e)
                status = False
            
            # Append the result for this particular failure.
            results.append({card_title: status})
        
        # Return the list of results, which maps card titles to the corresponding success status.
        return results


if __name__ == "__main__":
    # Example usage for testing the TrelloClient
    try:
        # Create a TrelloClient instance (credentials will be loaded from .env)
        client = TrelloClient()
        
        # Test creating a simple card
        if client.create_card("Sample Test Card", "This is a test card created by TrelloClient."):
            print("Test card created successfully.")
        else:
            print("Test card creation failed.")
        
        # Test creating a card for a dummy failure
        dummy_failures = [{
            "test_name": "Dummy Test Failure",
            "error_message": "An assertion failed unexpectedly",
            "traceback": "Traceback (most recent call last): ...\nAssertionError"
        }]
        failure_results = client.create_failure_cards(dummy_failures)
        print("Failure card creation results:", failure_results)
    except Exception as e:
        print("Error initializing TrelloClient:", e)
