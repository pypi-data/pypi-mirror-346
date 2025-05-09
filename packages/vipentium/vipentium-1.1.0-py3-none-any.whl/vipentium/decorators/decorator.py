# --------------------------------------------------------------
# Marker decorator for test filtering
# --------------------------------------------------------------
def mark(*tags):
    """
    Decorator to tag tests with marker labels.
    """
    def decorator(func):
        setattr(func, "markers", tags)
        return func
    return decorator

# --------------------------------------------------------------
# Decorators for Parameterized Tests, Timeout and Retry
# --------------------------------------------------------------
def parameters(*args, **kwargs):
    """
    Decorator for parameterized tests.
    Accepts either a tuple (args, kwargs) or a dict with keys: "args", "kwargs", "name"
    """
    def decorator(func):
        if not hasattr(func, "parameters"):
            func.parameters = []
        # If a single dict is passed with keys "args" (and optionally "kwargs" and "name")
        if len(args) == 1 and isinstance(args[0], dict) and "args" in args[0]:
            func.parameters.append((args[0]["args"], args[0].get("kwargs", {}), args[0].get("name", None)))
        else:
            func.parameters.append((args, kwargs, None))
        return func
    return decorator

def timeout(seconds):
    """
    Decorator to set a timeout (in seconds) for a test method.
    """
    def decorator(func):
        func.timeout = seconds
        return func
    return decorator

def retry(times):
    """
    Decorator to set the number of retry attempts for a failing test.
    """
    def decorator(func):
        func.retry = times
        return func
    return decorator