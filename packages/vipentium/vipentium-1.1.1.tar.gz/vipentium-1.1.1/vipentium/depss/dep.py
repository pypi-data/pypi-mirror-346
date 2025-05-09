# --------------------------------------------------------------
# Fixture Management and Dependency Injection
# --------------------------------------------------------------

# Global registry for fixtures.
FIXTURES = {}

def fixture(scope="function"):
    """
    Decorator to register a fixture.
    Supported scopes: "function" (default), "session"
    """
    def decorator(func):
        FIXTURES[func.__name__] = {"func": func, "scope": scope, "value": None}
        return func
    return decorator