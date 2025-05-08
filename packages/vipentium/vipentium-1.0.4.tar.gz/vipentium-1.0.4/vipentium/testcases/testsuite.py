from vipentium.starter.startz import *

from vipentium.testcases.coreex import *
# --------------------------------------------------------------
# TestSuite: Aggregates discovered test classes & runs all tests
# --------------------------------------------------------------
class TestSuite:
    def __init__(self, test_classes):
        self.test_classes = test_classes  # list of test class types
        self.results = []  # list of dict entries (one per test)
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.total_duration = 0

    def run(self):
        for plugin in PLUGINS:
            plugin.on_start_suite()
        max_workers = os.cpu_count() if config['parallel'] else 1
        # Choose executor: thread-based by default, or process-based if specified.
        if config['parallel'] and config['process']:
            executor = concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)
        else:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        future_to_test = {}
        # Process each test class
        for test_class in self.test_classes:
            # Call class-level setup if defined
            if hasattr(test_class, "setUpClass") and callable(getattr(test_class, "setUpClass")):
                try:
                    test_class.setUpClass()
                except Exception as e:
                    logger.error(color_text(f"Error in setUpClass of {test_class.__name__}: {e}", RED))
            # Discover test methods (names starting with "test_")
            methods = [m for m in dir(test_class) if m.startswith("test_") and callable(getattr(test_class, m))]
            for m in methods:
                method_obj = getattr(test_class, m)
                # If marker filter is enabled, check for method markers.
                if config.get("markers"):
                    method_markers = getattr(method_obj, "markers", [])
                    # Only run test if it has at least one marker that matches the filter.
                    if not any(tag in config["markers"] for tag in method_markers):
                        continue
                param_list = getattr(method_obj, "parameters", None)
                timeout_val = getattr(method_obj, "timeout", None)
                retry_count = getattr(method_obj, "retry", 0)
                if param_list is not None:
                    for idx, params in enumerate(param_list):
                        # Support named parameter sets if provided as a dict.
                        if isinstance(params, tuple) and len(params) == 3:
                            args_tuple, kwargs_dict, name = params
                            test_name = f"{test_class.__name__}.{m}[{name if name is not None else idx}]"
                            new_params = (args_tuple, kwargs_dict)
                        else:
                            # Expecting params as tuple (args, kwargs)
                            test_name = f"{test_class.__name__}.{m}[{idx}]"
                            new_params = params
                        for plugin in PLUGINS:
                            plugin.before_test(test_name, test_class, m, new_params)
                        future = executor.submit(execute_task, test_class, m, new_params, timeout_val, retry_count)
                        future_to_test[future] = (test_name, test_class, m, new_params)
                        self.total += 1
                else:
                    test_name = f"{test_class.__name__}.{m}"
                    for plugin in PLUGINS:
                        plugin.before_test(test_name, test_class, m, None)
                    future = executor.submit(execute_task, test_class, m, None, timeout_val, retry_count)
                    future_to_test[future] = (test_name, test_class, m, None)
                    self.total += 1
            # Call class-level teardown if defined
            if hasattr(test_class, "tearDownClass") and callable(getattr(test_class, "tearDownClass")):
                try:
                    test_class.tearDownClass()
                except Exception as e:
                    logger.error(color_text(f"Error in tearDownClass of {test_class.__name__}: {e}", RED))
        # Collect and log results as tasks complete
        for future in concurrent.futures.as_completed(future_to_test):
            test_name, test_class, method_name, params = future_to_test[future]
            try:
                success, message, duration = future.result()
            except Exception as exc:
                success = False
                message = str(exc)
                duration = 0
            self.total_duration += duration
            if success:
                self.passed += 1
                display = color_text(f"✅ [PASS] {test_name} ({duration:.2f}s)", GREEN)
            else:
                self.failed += 1
                display = color_text(f"❌ [FAIL] {test_name} ({duration:.2f}s) - {message}", RED)
            self.results.append({
                "test": test_name,
                "success": success,
                "message": message,
                "duration": duration
            })
            print(display)
            for plugin in PLUGINS:
                plugin.after_test(test_name, test_class, method_name, params, success, message, duration)
        summary = {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "duration": self.total_duration
        }
        for plugin in PLUGINS:
            plugin.on_end_suite(summary)
        summary_text = (
            f"\n🌟 Test Summary 🌟\n"
            f"🧪 Total: {self.total} | ✅ Passed: {self.passed} | ❌ Failed: {self.failed} | ⏱ Duration: {self.total_duration:.2f}s"
        )
        print(color_text(summary_text, CYAN))
        return summary