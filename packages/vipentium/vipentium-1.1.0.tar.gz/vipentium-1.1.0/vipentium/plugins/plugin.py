# --------------------------------------------------------------
# Plugin Architecture
# --------------------------------------------------------------
class Plugin:
    def before_test(self, test_name, test_class, method_name, parameters):
        pass

    def after_test(self, test_name, test_class, method_name, parameters, success, message, duration):
        pass

    def on_start_suite(self):
        pass

    def on_end_suite(self, summary):
        pass