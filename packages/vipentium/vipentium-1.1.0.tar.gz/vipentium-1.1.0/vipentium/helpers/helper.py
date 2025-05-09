from vipentium.testcases.coreex import *
# --------------------------------------------------------------
# Auto-discovery Helpers
# --------------------------------------------------------------

def discover_test_files(root):
    test_files = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            print(f"DEBUG: Checking file: {filename}")  # Debug print
            if filename.startswith("test_") and filename.endswith(".py"):
                full_path = os.path.join(dirpath, filename)
                print(f"DEBUG: Found test file: {full_path}")  # Debug print
                test_files.append(full_path)
    return test_files


def load_module_from_file(filepath):
    """
    Load a Python module from a given file path.
    """
    module_name = os.path.splitext(os.path.basename(filepath))[0]
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_test_classes_from_module(module):
    import inspect
    classes = []
    for name, obj in module.__dict__.items():
        if inspect.isclass(obj) and name != "TestCase" and name.startswith("Test"):
            if any(base.__name__ == "TestCase" for base in inspect.getmro(obj)):
                classes.append(obj)
    return classes


def discover_tests(path):
    """
    Discover all test classes that are subclasses of TestCase.
    'path' may be a directory, a .py file, or a module name.
    """
    test_classes = []
    if os.path.isdir(path):
        files = discover_test_files(path)
        if config.get('verbose', False):
            logger.debug(color_text(f"Discovered test files: {files}", CYAN))
        for f in files:
            try:
                mod = load_module_from_file(f)
                test_classes.extend(get_test_classes_from_module(mod))
            except Exception as e:
                if config['verbose']:
                    logger.error(color_text(f"Error loading {f}: {e}", RED))
    else:
        if path.endswith(".py"):
            try:
                mod = load_module_from_file(path)
                test_classes.extend(get_test_classes_from_module(mod))
            except Exception as e:
                if config.get('verbose', False):
                    logger.error(color_text(f"Error loading module from file {path}: {e}", RED))
        else:
            try:
                mod = importlib.import_module(path)
                test_classes.extend(get_test_classes_from_module(mod))
            except Exception as e:
                logger.error(color_text(f"Error importing module {path}: {e}", RED))
    return test_classes