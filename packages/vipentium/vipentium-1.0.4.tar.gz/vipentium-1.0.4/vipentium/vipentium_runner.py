#!/usr/bin/env python3
"""
vipentium: A Comprehensive Python Testing Framework

Features:
  • Auto test discovery (module, file, or directory)
  • Parameterized testing via @parameters decorator with optional names
  • Asynchronous test support (async/await tests)
  • Timeouts and retries via @timeout and @retry decorators
  • Parallel test execution (--parallel flag) with option for process-based execution (--process)
  • Enhanced fixture management with dependency injection via @fixture
  • Test filtering via markers (@mark and --mark)
  • Advanced reporting: JSON and HTML reports (--report-json / --report-html)

"""

from depss.dep import *
from decorators.decorator import *
from helpers.helper import *
from plugins.plugin import *
from reports.report import *
from testcases.coreex import *
from testcases.testbase import *
from testcases.testsuite import *




# --------------------------------------------------------------
# Main Runner: Parse arguments, initialize, discover tests, and run suite
# --------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="vipentium Test Runner - Comprehensive Python Testing Framework")
    parser.add_argument("path", help="Path to a test module, file, or directory containing tests")
    parser.add_argument("--parallel", action="store_true", help="Enable parallel test execution (thread-based by default)")
    parser.add_argument("--process", action="store_true", help="Use process-based parallelism (requires --parallel)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--report-json", type=str, default=None, help="Generate JSON report to specified file")
    parser.add_argument("--report-html", type=str, default=None, help="Generate HTML report to specified file")
    parser.add_argument("--coverage", action="store_true", help="Enable coverage integration (placeholder)")
    parser.add_argument("--mark", action="append", help="Only run tests that contain the specified marker. Can be used multiple times.")
    args = parser.parse_args()
    
    config['parallel'] = args.parallel
    config['process'] = args.process
    config['verbose'] = args.verbose
    config['report_json'] = args.report_json
    config['report_html'] = args.report_html
    config['coverage'] = args.coverage
    config['markers'] = args.mark if args.mark else None

    if config['coverage']:
        logger.info(color_text("Coverage integration is enabled (placeholder)", YELLOW))

    if config['verbose']:
        logger.info(color_text("Verbose mode enabled.", YELLOW))
    
    # Setup a loader spinner during initialization
    loader_start = time.time()
    spinner = ['|', '/', '-', '\\']
    spin_duration = 2  # seconds
    while time.time() - loader_start < spin_duration:
        for frame in spinner:
            if time.time() - loader_start >= spin_duration:
                break
            print(f"\r⌛ Initializing vipentium... {frame}", end='', flush=True)
            time.sleep(0.1)
    print("\r" + " " * 80, end="\r")
    print(color_text("🚀 Welcome to vipentium! Let's run the tests! 🚀\n", CYAN))
    
    # Discover tests automatically from the given path
    test_classes = discover_tests(args.path)
    if not test_classes:
        logger.error(color_text("No tests found.", RED))
        sys.exit(1)
    if config['verbose']:
        logger.info(color_text(f"Discovered {len(test_classes)} test classes.", YELLOW))
    
    suite = TestSuite(test_classes)
    summary = suite.run()

    # Generate reports if requested
    if config['report_json']:
        generate_json_report(config['report_json'], summary, suite.results)
    if config['report_html']:
        generate_html_report(config['report_html'], summary, suite.results)
    
    sys.exit(0 if summary['failed'] == 0 else 1)

if __name__ == "__main__":
    main()
