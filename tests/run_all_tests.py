"""
Main test runner for MBTI Roster regression tests
Executes all test suites and generates comprehensive reports
"""

import sys
import os
import time
from datetime import datetime
from tests.config import test_config
from tests.test_auth import run_auth_tests
from tests.test_celebrities import run_celebrities_tests
from tests.test_voting import run_voting_tests
from tests.test_comments import run_comments_tests
from tests.test_search import run_search_tests


def print_banner():
    """Print test suite banner"""
    print("=" * 80)
    print("MBTI Roster Regression Test Suite")
    print("=" * 80)
    print(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {test_config.base_url}")
    print(f"Admin User: {test_config.admin_credentials['email']}")
    print("=" * 80)


def check_server_availability():
    """Check if the server is running and accessible"""
    print("Checking server availability...")
    try:
        import requests

        response = requests.get(f"{test_config.base_url}/health", timeout=5)
        if response.status_code == 200:
            print("Server is running and accessible")
            return True
        else:
            print(f"Server responded with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"Cannot connect to server: {e}")
        print("Make sure the server is running with: python run_local.py")
        return False


def login_admin():
    """Login as admin user"""
    print("Logging in as admin user...")
    if test_config.login_admin():
        print("Admin login successful")
        return True
    else:
        print("Admin login failed")
        return False


def run_test_suite(suite_name, test_function):
    """Run a specific test suite"""
    print(f"\n{'='*20} {suite_name} {'='*20}")
    start_time = time.time()

    try:
        success = test_function()
        end_time = time.time()
        duration = end_time - start_time

        if success:
            print(f"{suite_name} completed successfully ({duration:.2f}s)")
        else:
            print(f"{suite_name} had failures ({duration:.2f}s)")

        return success
    except Exception as e:
        print(f"{suite_name} failed with exception: {e}")
        return False


def print_summary():
    """Print test summary"""
    summary = test_config.get_test_summary()

    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed_tests']}")
    print(f"Failed: {summary['failed_tests']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print("=" * 80)

    # Print failed tests
    failed_tests = [result for result in summary["results"] if not result["success"]]
    if failed_tests:
        print("\nFAILED TESTS:")
        for test in failed_tests:
            print(f"  • {test['test_name']}: {test['details']}")

    return summary["success_rate"] == 100


def save_test_report():
    """Save detailed test report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_reports/regression_test_report_{timestamp}.json"

    # Create reports directory if it doesn't exist
    os.makedirs("test_reports", exist_ok=True)

    return test_config.save_test_report(filename)


def main():
    """Main test runner function"""
    print_banner()

    # Check server availability
    if not check_server_availability():
        print("\nCannot proceed with tests. Server is not available.")
        sys.exit(1)

    # Login as admin
    if not login_admin():
        print("\nCannot proceed with tests. Admin login failed.")
        sys.exit(1)

    # Define test suites
    test_suites = [
        ("Authentication System", run_auth_tests),
        ("Celebrity Management", run_celebrities_tests),
        ("Voting System", run_voting_tests),
        ("Comment System", run_comments_tests),
        ("Search Functionality", run_search_tests),
    ]

    # Run all test suites
    start_time = time.time()
    passed_suites = 0
    total_suites = len(test_suites)

    for suite_name, test_function in test_suites:
        if run_test_suite(suite_name, test_function):
            passed_suites += 1

    end_time = time.time()
    total_duration = end_time - start_time

    # Print summary
    all_passed = print_summary()

    # Save detailed report
    report_file = save_test_report()

    # Final summary
    print("\nFINAL RESULTS:")
    print(f"Test Suites: {passed_suites}/{total_suites} passed")
    print(f"Total Duration: {total_duration:.2f}s")
    print(f"Detailed Report: {report_file}")

    if all_passed:
        print("All tests passed! The application is working correctly.")
        sys.exit(0)
    else:
        print("Some tests failed. Please check the detailed report.")
        sys.exit(1)


if __name__ == "__main__":
    main()
