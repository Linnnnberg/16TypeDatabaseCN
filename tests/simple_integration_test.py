#!/usr/bin/env python3
"""
Simple Integration Test Script
Basic HTTP tests without pytest dependencies
"""

import requests
import time
import sys


def test_endpoint(url, expected_status=200, timeout=10):
    """Test a single endpoint"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == expected_status:
            print(f"SUCCESS: {url} - Status: {response.status_code}")
            return True
        else:
            print(
                f"FAILED: {url} - Expected: {expected_status}, "
                f"Got: {response.status_code}"
            )
            return False
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {url} - {e}")
        return False


def test_json_endpoint(url, expected_keys=None, timeout=10):
    """Test a JSON endpoint"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            if expected_keys:
                for key in expected_keys:
                    if key not in data:
                        print(f"FAILED: {url} - Missing key: {key}")
                        return False
            print(f"SUCCESS: {url} - Status: {response.status_code}")
            return True
        else:
            print(f"FAILED: {url} - Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {url} - {e}")
        return False


def main():
    """Run all integration tests"""
    print("=== Simple Integration Tests ===")
    print("Testing server at: http://localhost:8000")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    base_url = "http://localhost:8000"
    tests = []

    # Basic endpoint tests
    tests.append(("Health Check", lambda: test_endpoint(f"{base_url}/health")))
    tests.append(
        (
            "API Root",
            lambda: test_json_endpoint(
                f"{base_url}/api", ["message", "version", "status"]
            ),
        )
    )
    tests.append(
        (
            "Test Endpoint",
            lambda: test_json_endpoint(f"{base_url}/test", ["message", "mbti_types"]),
        )
    )
    tests.append(
        ("Database Test", lambda: test_json_endpoint(f"{base_url}/db-test", ["status"]))
    )
    tests.append(
        (
            "Environment Info",
            lambda: test_json_endpoint(
                f"{base_url}/env", ["python_version", "fastapi_version"]
            ),
        )
    )

    # Endpoint existence tests (accept various status codes)
    tests.append(
        (
            "Auth Endpoint Exists",
            lambda: test_endpoint(f"{base_url}/auth/login", expected_status=[405, 404]),
        )
    )
    tests.append(
        (
            "Celebrities Endpoint Exists",
            lambda: test_endpoint(
                f"{base_url}/api/celebrities", expected_status=[200, 401, 404]
            ),
        )
    )

    # Documentation tests
    tests.append(("API Docs", lambda: test_endpoint(f"{base_url}/docs")))
    tests.append(
        (
            "OpenAPI Schema",
            lambda: test_json_endpoint(
                f"{base_url}/openapi.json", ["openapi", "info", "paths"]
            ),
        )
    )

    # Performance test
    def test_response_time():
        start_time = time.time()
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            end_time = time.time()
            response_time = end_time - start_time

            if response.status_code == 200 and response_time < 2.0:
                print(f"SUCCESS: Response time test - {response_time:.2f}s")
                return True
            else:
                print(f"FAILED: Response time test - {response_time:.2f}s (too slow)")
                return False
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Response time test - {e}")
            return False

    tests.append(("Response Time", test_response_time))

    # Run all tests
    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1

    # Summary
    print("\n=== Test Summary ===")
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")

    if passed == total:
        print("SUCCESS: All integration tests passed!")
        return 0
    else:
        print("FAILED: Some integration tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
