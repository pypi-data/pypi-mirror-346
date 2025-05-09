![image](https://github.com/user-attachments/assets/cc2e0757-9bc0-4957-b406-d0a5f10049a2)

vipentium is a robust and user-friendly Python testing framework engineered to streamline your testing process. It provides a rich set of features to facilitate efficient test creation and execution.

[![PyPI Downloads](https://static.pepy.tech/badge/vipentium)](https://pepy.tech/projects/vipentium)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python Versions](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)


### Note
```
please always check docs in the website for updated one always
```

## ✨ Key Features

* **🔍 Auto Test Discovery:** Automatically identifies test files (prefixed with `test_`), modules, and directories within a specified path, simplifying test organization and execution.
* **⚙️ Parameterized Testing (`@parameters`):** Enables running a single test function with multiple sets of input data. You can provide tuples of arguments or dictionaries of keyword arguments, optionally naming each parameter set for clearer reporting.
* **⏳ Asynchronous Test Support (`async`/`await`):** Fully supports testing asynchronous Python code written using `async` and `await` keywords, ensuring compatibility with modern Python concurrency.
* **⏰ Timeout Control (`@timeout`):** Allows setting a maximum execution time (in seconds) for individual test methods. If a test exceeds this limit, it's automatically marked as failed, preventing indefinite hangs.
* **🔄 Test Retries (`@retry`):** Provides a mechanism to automatically re-run failing tests a specified number of times. This is particularly useful for handling tests that might occasionally fail due to external factors or non-deterministic behavior.
* **💨 Parallel Execution (`--parallel`, `--process`):** Significantly reduces test execution time by running tests concurrently. The `--parallel` flag uses threads, while the `--process` flag utilizes separate processes for better isolation (requires `--parallel`).
* **🔌 Plugin Architecture:** Offers a flexible plugin system that allows you to extend the framework's functionality. You can create custom plugins to hook into various stages of the test lifecycle (e.g., before/after tests, suite start/end).
* **🛠️ Enhanced Fixture Management (`@fixture`):** Introduces a powerful fixture system for managing test dependencies and setup/cleanup operations. Fixtures support dependency injection, allowing test methods to receive required resources as arguments. Fixture scopes (`function`, `session`) control their lifecycle.
* **🏷️ Test Filtering with Markers (`@mark`, `--mark`):** Enables tagging test methods with descriptive labels using the `@mark` decorator. You can then use the `--mark` command-line option to selectively run tests based on these markers.
* **🗣️ Verbose Output (`--verbose`):** Provides more detailed output during test execution, including the names of discovered tests, the status of each test (pass/fail), execution times, and any error messages, enhanced with ANSI color codes for better readability.
* **📊 Advanced Reporting (`--report-json`, `--report-html`):** Supports generating comprehensive test reports in two formats:
    * **JSON (`--report-json <filename>`):** Creates a structured JSON file containing a summary of the test run and detailed results for each test.
    * **HTML (`--report-html <filename>`):** Generates a user-friendly HTML report with a summary and detailed test results presented in a web browser.

## 🕹️ Getting Started


```
pip install vipentium
```

## Usage Instructions

| **Type**       | **Command**                                         | **Example**                                   |
|-----------------|----------------------------------------------------|-----------------------------------------------|
| Recommended    | `vipentium-runner <test_path> [options]`            | `vipentium-runner test_example.py --parallel` |
| Alternative    | `python -m vipentium.vipentium_runner <test_path> [options]` | `python -m vipentium.vipentium_runner test_example.py --parallel` |


### Example:
- **Recommended:** `vipentium-runner test_example.py --parallel`  
- **Alternative:** `python -m vipentium.vipentium_runner test_example.py --parallel`

Replace `<test_path>` with the path to the directory, file, or module containing your tests.

### Command-Line Options

| Option          | Description                                                                                                |
| :-------------- | :--------------------------------------------------------------------------------------------------------- |
| `<test_path>`   | The path to the directory, file, or module where vipentium should discover and run tests.                   |
| `--parallel`    | Enable parallel test execution using threads for potentially faster test runs.                             |
| `--process`     | Use separate processes for parallel test execution (requires `--parallel`). Provides better isolation.       |
| `--verbose`     | Enable verbose output, showing more details about the test execution process.                               |
| `--report-json <filename>` | Generate a test report in JSON format and save it to the specified filename.                       |
| `--report-html <filename>` | Generate a test report in HTML format and save it to the specified filename.                       |
| `--mark <marker>` | Only run tests that are decorated with the specified marker. This option can be used multiple times.      |
| `--trello` | Enables Trello integration. When used, vipentium converts test failures into Trello cards with all relevant details. |


## Trello Integration Credentials Setup 🔐

Enhance your Vipentium testing workflow by enabling Trello integration! With this feature, every test failure is automatically logged as a Trello card—making it easier than ever to track and resolve issues.


### 1. Create a `.env` File 📄

In the root directory of your project, create a file named:
```
.env
```

### 2. Add Your Trello Credentials 🛡️

Open the `.env` file and add the following lines (replace the placeholders with your actual credentials):

```env
TRELLO_KEY=your_trello_api_key_here
TRELLO_TOKEN=your_trello_api_token_here
TRELLO_LIST_ID=your_trello_list_id_here
```

- **TRELLO_KEY:** Your unique Trello API key.
- **TRELLO_TOKEN:** Your Trello API token.
- **TRELLO_LIST_ID:** The ID of the Trello list where new cards will be created for test failures.

---

### 3. Secure Your Credentials 🔒

To protect your sensitive information, add the `.env` file to your `.gitignore`:

```gitignore
.env
```

---

### 4. Setting Up Environment Variables in PowerShell 🚀

If you run your tests using PowerShell, manually set the Trello environment variables by following these steps:

1. **Open PowerShell:** Launch PowerShell via the Start Menu or your preferred method.

2. **Set the Environment Variables:** Run the following commands (replacing the placeholders with your actual credentials):

   ```powershell
   $env:TRELLO_KEY = "your_trello_api_key_here"
   $env:TRELLO_TOKEN = "your_trello_api_token_here"
   $env:TRELLO_LIST_ID = "your_trello_list_id_here"
   ```

3. **Verify the Variables (Optional):** Check that they’re set correctly by running:

   ```powershell
   echo $env:TRELLO_KEY
   echo $env:TRELLO_TOKEN
   echo $env:TRELLO_LIST_ID
   ```

---

### 5. Usage ⚙️

With your credentials configured, Vipentium will automatically load these environment variables. Use the `--trello` option to enable Trello integration when running your tests:

```bash
vipentium-runner <test_path> --trello
```

Replace `<test_path>` with the path to your test files, directory, or module.

---

You're all set! Enjoy seamless test tracking and issue resolution with Trello integration. 🚀
```
---


## 🧪 Writing Test Cases

1.  **Test File Naming:** Name your test files with the prefix `test_` (e.g., `test_utils.py`).
2.  **Test Class Definition:** Create classes that inherit from the `TestCase` base class provided by vipentium.
3.  **Test Method Definition:** Define individual test methods within your test classes. These methods must start with the prefix `test_` (e.g., `test_calculate_sum`).
4.  **Assertions:** Use the `assert_equal(a, b)` method provided by the `TestCase` class to compare expected and actual results. You can also use standard Python `assert` statements.
5.  **Decorators for Enhanced Testing:**
      * `@parameters(*args, **kwargs)`: Apply this decorator to a test method to run it with multiple sets of arguments. You can provide individual tuples or a list of tuples. For named parameters, use a dictionary with keys `"args"`, `"kwargs"`, and optionally `"name"`.
      * `@timeout(seconds)`: Decorate a test method to set a maximum execution time in seconds.
      * `@retry(times)`: Decorate a test method to specify the number of times it should be automatically retried upon failure.
      * `@mark(*tags)`: Decorate a test method with one or more marker tags (strings).
      * `@fixture(scope="function"|"session")`: Decorate a function to define a test fixture. The `scope` argument determines the fixture's lifecycle.

<!-- end list -->


## 🚀 Usage Guidelines

### 🗂 Test File Naming

- **Naming Convention:**  
  Name your test files with the prefix `test_` (e.g., `test_utils.py`). This allows vipentium to automatically discover them.

### 🏗 Test Class Definition

- **Inheritance:**  
  Create test classes by subclassing the `TestCase` base class provided by vipentium. For example:

```python
from vipentium import TestCase

class TestMyFunction(TestCase):
    ...
```

### 📝 Test Method Definition

- **Method Naming:**  
  Define individual test methods with names starting with `test_` (e.g., `test_calculate_sum`).
  
- **Assertions:**  
  Use the built-in assertion method `assert_equal(a, b)` to compare expected and actual results.  
  You can also use standard Python `assert` statements if needed.

### 🎯 Decorators for Enhanced Testing

- **`@parameters(*args, **kwargs)`**  
  Run a test method with multiple sets of arguments. You can supply individual tuples or a list of tuples. For named parameters, use a dictionary with keys `"args"`, `"kwargs"`, and optionally `"name"`.

- **`@timeout(seconds)`**  
  Set a maximum execution time for a test method.

- **`@retry(times)`**  
  Automatically retry a test method upon failure a specified number of times.

- **`@mark(*tags)`**  
  Decorate a test method (or class) with marker tags (strings) to help organize and filter tests.

- **`@fixture(scope="function"|"session")`**  
  Define reusable test setup functions:
  - **`function`**: A new instance is provided for each test.
  - **`session`**: The fixture is shared across all tests in a test session.

#### Example Usage

```python
from vipentium import TestCase, parameters, mark, fixture

@fixture(scope="function")
def simple_list():
    """A simple list fixture."""
    return [1, 2, 3]

@fixture(scope="session")
def shared_resource():
    """A shared resource fixture available for the entire session."""
    print("\nSetting up shared resource...")
    data = {"message": "Hello from shared resource"}
    return data

@mark("basic")
class TestBasicOperations(TestCase):
    def test_addition(self):
        self.assert_equal(2 + 2, 4)

    def test_string_concat(self):
        self.assert_equal("hello" + "world", "helloworld")

    def test_list_length(self, simple_list):
        self.assert_equal(len(simple_list), 3)

    def test_shared_message(self, shared_resource):
        self.assert_equal(shared_resource["message"], "Hello from shared resource")

@mark("math")
class TestMathFunctions(TestCase):
    @parameters((5, 2, 7), (10, -3, 7), (0, 0, 0))
    def test_add_parameterized(self, a, b, expected):
        self.assert_equal(a + b, expected)

    def test_division(self):
        self.assert_equal(10 / 2, 5)

    def test_float_equality(self):
        self.assert_equal(3.14, 3.14)

@mark("list_operations")
class TestListManipulation(TestCase):
    def test_append(self, simple_list):
        simple_list.append(4)
        self.assert_equal(simple_list, [1, 2, 3, 4])

    def test_pop(self, simple_list):
        popped_item = simple_list.pop()
        self.assert_equal(popped_item, 3)
        self.assert_equal(simple_list, [1, 2])

    def test_contains(self, simple_list):
        self.assert_equal(2 in simple_list, True)
        self.assert_equal(5 in simple_list, False)
```

## Testing and Output

### 🏃‍♂️ Running the Tests

To run your tests, simply execute vipentium with your test file. For example:

```bash
vipentium-runner test_example.py
```

### 📊 Expected Output

vipentium will automatically:
- Discover test files with the `test_` prefix.
- Inject fixtures based on parameter names.
- Execute parameterized tests and other test methods.
- Provide detailed output to the console similar to:

```
🚀 Welcome to vipentium! Let's run the tests! 🚀

✅ [PASS] TestBasicOperations.test_addition (0.00s)
✅ [PASS] TestBasicOperations.test_list_length (0.00s)
✅ [PASS] TestBasicOperations.test_string_concat (0.00s)
✅ [PASS] TestBasicOperations.test_shared_message (0.00s)
✅ [PASS] TestMathFunctions.test_division (0.00s)
✅ [PASS] TestMathFunctions.test_float_equality (0.00s)
✅ [PASS] TestMathFunctions.test_add_parameterized (0.00s)
✅ [PASS] TestListManipulation.test_append (0.00s)
✅ [PASS] TestListManipulation.test_pop (0.00s)
✅ [PASS] TestListManipulation.test_contains (0.00s)

🌟 Test Summary 🌟
🧪 Total: 10 | ✅ Passed: 10 | ❌ Failed: 0 | ⏱ Duration: 0.00s
HTML report generated at hello.html
```

The output includes:
- A test-by-test status with execution times.
- A summary of total tests, passed tests, failed tests, and overall duration.
- Optional report files (HTML, JSON) for further review.

---

## 🔌 Extending with Plugins

vipentium's plugin system allows you to customize and extend its behavior. To create a plugin:

1.  Create a class that inherits from the `Plugin` base class provided by `vipentium`.
2.  Override the available hook methods (`before_test`, `after_test`, `on_start_suite`, `on_end_suite`) to implement your desired actions.
3.  Register your plugin using the `register_plugin()` function.

<!-- end list -->

```python
from vipentium import Plugin, register_plugin

class CustomReportPlugin(Plugin):
    def after_test(self, test_name, test_class, method_name, parameters, success, message, duration):
        if success:
            print(f"[CUSTOM REPORT] Test '{test_name}' passed in {duration:.2f}s")
        else:
            print(f"[CUSTOM REPORT] Test '{test_name}' failed: {message}")

def load_my_plugins():
    register_plugin(CustomReportPlugin())

# Make sure to call load_my_plugins() before running your tests.
```

## 📊 Reporting

vipentium can generate detailed reports of your test execution:

  * **JSON Report:** A structured `.json` file containing a summary of the test run (total, passed, failed, duration) and a list of individual test results with their names, status, duration, and any failure messages.
  * **HTML Report:** A human-readable `.html` file presenting the test summary and detailed results in a well-formatted web page.

Use the `--report-json <filename>` and `--report-html <filename>` command-line options to specify the names of the generated report files.

## 📜 License

MIT | @vipentium
