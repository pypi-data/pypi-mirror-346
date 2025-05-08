# --------------------------------------------------------------
# TestCase Base Class (Enhanced with Fixture Injection)
# --------------------------------------------------------------
class TestCase:
    """
    Base class for test cases.
    Override:
      - setUp() and tearDown() for per-test initialization and cleanup.
      - Optionally, setUpClass() and tearDownClass() as classmethods for fixture management.
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assert_equal(self, a, b):
        if a != b:
            raise AssertionError(f"Expected {a} to equal {b}")