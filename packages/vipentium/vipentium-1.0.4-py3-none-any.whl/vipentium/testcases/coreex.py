from vipentium.starter.startz import *
# Add the parent directory to sys.path so that the "vipentium" folder is recognized.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Global configuration dictionary
config = {
    'parallel': False,
    'process': False,  # If True, use ProcessPoolExecutor for parallelism.
    'verbose': False,
    'report_json': None,
    'report_html': None,
    'coverage': False,  # Placeholder for coverage integration
    'markers': None     # Marker filter (list)
}

# Global plugin registry
PLUGINS = []

def register_plugin(plugin):
    PLUGINS.append(plugin)

# Setup logging
logger = logging.getLogger("vipentium")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# ANSI color codes for colorized output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

def color_text(text, color):
    return f"{color}{text}{RESET}"

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

# --------------------------------------------------------------
# Core test execution (with fixture injection, timeouts, retries, and async support)
# --------------------------------------------------------------
def run_test_method(test_class, method_name, param_data, retry_count):
    """
    Execute a single test method and return (success, message, duration)
    Supports dependency injection with fixtures if no param_data is provided.
    """
    attempts = 0
    last_error = ""
    start_time = time.time()
    while attempts <= retry_count:
        instance = test_class()  # fresh instance for each attempt
        try:
            instance.setUp()
            method = getattr(instance, method_name)
            # If parameterized data is provided, then use it and skip fixture injection.
            if param_data is not None:
                args, kwargs = param_data
            else:
                # Dependency Injection: Inspect the method's signature for fixture injection
                argspec = inspect.getfullargspec(method)
                if len(argspec.args) > 1:
                    injected = []
                    for fixture_name in argspec.args[1:]:
                        if fixture_name in FIXTURES:
                            info = FIXTURES[fixture_name]
                            if info["scope"] == "session":
                                if info.get("value") is None:
                                    if inspect.iscoroutinefunction(info["func"]):
                                        info["value"] = asyncio.run(info["func"]())
                                    else:
                                        info["value"] = info["func"]()
                                injected.append(info["value"])
                            else:  # function scope
                                if inspect.iscoroutinefunction(info["func"]):
                                    injected.append(asyncio.run(info["func"]()))
                                else:
                                    injected.append(info["func"]())
                        else:
                            raise Exception(f"Fixture '{fixture_name}' not found")
                    args, kwargs = tuple(injected), {}
                else:
                    args, kwargs = (), {}
            # Execute the test method (handle async methods appropriately)
            if inspect.iscoroutinefunction(method):
                asyncio.run(method(*args, **kwargs))
            else:
                method(*args, **kwargs)
            instance.tearDown()
            duration = time.time() - start_time
            return True, "", duration
        except Exception:
            last_error = traceback.format_exc()
            attempts += 1
            try:
                instance.tearDown()
            except Exception:
                pass
    duration = time.time() - start_time
    return False, f"Failed after {attempts} attempts: {last_error}", duration

def execute_task(test_class, method_name, param_data, timeout_val, retry_count):
    """
    Wrapper to execute a test method with an optional timeout.
    """
    if timeout_val is not None:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_test_method, test_class, method_name, param_data, retry_count)
            try:
                result = future.result(timeout=timeout_val)
                return result
            except concurrent.futures.TimeoutError:
                return False, f"Timeout after {timeout_val} seconds", timeout_val
    else:
        return run_test_method(test_class, method_name, param_data, retry_count)