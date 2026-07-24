import sys
import time
import traceback
from typing import Any, List, Tuple

try:
    from main import solve_problem
except ImportError:
    print("Error: Could not import solve_problem from main.py")
    print("Make sure main.py exists and contains the solve_problem function")
    sys.exit(1)


class TestCase:
    """Represents a single test case for Parallel Processing problem."""

    def __init__(self, tasks: List[int], expected_output: int, description: str = ""):
        self.tasks = tasks
        self.expected_output = expected_output
        self.description = description


class TestRunner:
    """Runs and manages test cases for Parallel Processing problem."""

    def __init__(self):
        self.test_cases = []
        self.passed = 0
        self.failed = 0
        self.errors = 0

    def add_test_case(
        self, tasks: List[int], expected_output: int, description: str = ""
    ):
        """Add a test case to the test suite."""
        self.test_cases.append(TestCase(tasks, expected_output, description))

    def run_single_test(
        self, test_case: TestCase, test_number: int, show_details: bool = False
    ):
        """Run a single test case."""
        try:
            start_time = time.time()
            result = solve_problem(test_case.tasks)
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

            if result == test_case.expected_output:
                self.passed += 1
                if show_details:
                    print(f"✅ Test {test_number} ({execution_time:.2f}ms)")
                    print(f"  Input: {test_case.tasks}")
                    print(f"  Expected: {test_case.expected_output}, Got: {result}")
            else:
                self.failed += 1
                print(f"❌ Test {test_number} ({execution_time:.2f}ms)")
                if test_case.description:
                    print(f"  Description: {test_case.description}")
                print(f"  Input: {test_case.tasks}")
                print(f"  Expected: {test_case.expected_output}, Got: {result}")

        except Exception as e:
            self.errors += 1
            print(f"⚠️ Test {test_number} ERROR")
            if test_case.description:
                print(f"  Description: {test_case.description}")
            print(f"  Input: {test_case.tasks}")
            print(f"  Error: {str(e)}")
            if show_details:
                print(f"  Traceback: {traceback.format_exc()}")

    def run_all_tests(self, show_details: bool = False, show_summary: bool = True):
        """Run all test cases."""
        print("Parallel Processing - Test Suite")
        print("=" * 50)

        if not self.test_cases:
            print("No test cases found!")
            return

        for i, test_case in enumerate(self.test_cases, 1):
            self.run_single_test(test_case, i, show_details)
            if i < len(self.test_cases):
                print()

        if show_summary:
            self.print_summary()

    def print_summary(self):
        """Print test execution summary."""
        total = len(self.test_cases)
        print("=" * 50)
        print("TEST SUMMARY")
        print("-" * 50)
        print(
            f"Total: {total} | Passed: {self.passed} | Failed: {self.failed} | Errors: {self.errors}"
        )

        if self.passed == total:
            print("✅ ALL TESTS PASSED!")
        elif self.failed > 0:
            print("❌ Some tests failed.")
        if self.errors > 0:
            print("⚠️ Some tests had errors.")

        print("=" * 50)


def create_test_cases():
    """Create comprehensive test cases for Parallel Processing problem."""
    test_runner = TestRunner()

    # Hidden Test Case 1: Single task
    test_runner.add_test_case(tasks=[5], expected_output=5, description="Single task")

    # Hidden Test Case 2: Two identical tasks
    test_runner.add_test_case(
        tasks=[3, 3], expected_output=3, description="Two identical tasks"
    )

    # Hidden Test Case 3: Increasing sequence
    test_runner.add_test_case(
        tasks=[1, 2, 3, 4, 5], expected_output=9, description="Increasing sequence"
    )

    # Hidden Test Case 4: All same values
    test_runner.add_test_case(
        tasks=[2, 2, 2, 2, 2, 2, 2, 2], expected_output=8, description="All same values"
    )

    # Hidden Test Case 5: Large difference in task times
    test_runner.add_test_case(
        tasks=[100, 1, 1, 1, 1],
        expected_output=100,
        description="One large task with many small tasks",
    )

    return test_runner


def main():
    """Main function to run the comprehensive test suite."""
    print("Parallel Processing Testing System")
    print()

    # Create test cases
    test_runner = create_test_cases()

    # Run tests
    test_runner.run_all_tests(show_details=False, show_summary=True)


if __name__ == "__main__":
    main()
