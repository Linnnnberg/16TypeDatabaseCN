"""
Authentication system regression tests
Tests user registration, login, and profile management
"""
import requests
from tests.config import test_config

def test_health_check():
    """Test basic health check endpoint"""
    try:
        response = requests.get(f"{test_config.base_url}/health")
        success = response.status_code == 200
        test_config.add_test_result(
            "Health Check",
            success,
            f"Status: {response.status_code}, Response: {response.text}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Health Check", False, str(e))
        return False

def test_admin_login():
    """Test admin user login"""
    try:
        response = requests.post(
            f"{test_config.base_url}/auth/login",
            json=test_config.admin_credentials
        )
        success = response.status_code == 200
        if success:
            data = response.json()
            test_config.auth_token = data.get("access_token")
            test_config.add_test_result(
                "Admin Login",
                True,
                f"Token received: {test_config.auth_token[:20]}..."
            )
        else:
            test_config.add_test_result(
                "Admin Login",
                False,
                f"Status: {response.status_code}, Response: {response.text}"
            )
        return success
    except Exception as e:
        test_config.add_test_result("Admin Login", False, str(e))
        return False

def test_get_current_user():
    """Test getting current user profile"""
    try:
        response = test_config.make_request("GET", "/auth/me")
        success = response.status_code == 200
        test_config.add_test_result(
            "Get Current User",
            success,
            f"Status: {response.status_code}, User: {response.json().get('email', 'N/A')}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Get Current User", False, str(e))
        return False

def test_user_registration():
    """Test new user registration"""
    try:
        test_user_data = {
            "email": "newuser@test.com",
            "password": "newuser123",
            "name": "New Test User"
        }
        response = requests.post(
            f"{test_config.base_url}/auth/signup",
            json=test_user_data
        )
        success = response.status_code == 201
        test_config.add_test_result(
            "User Registration",
            success,
            f"Status: {response.status_code}, Response: {response.text}"
        )
        return success
    except Exception as e:
        test_config.add_test_result("User Registration", False, str(e))
        return False

def test_invalid_login():
    """Test login with invalid credentials"""
    try:
        invalid_credentials = {
            "email": "invalid@test.com",
            "password": "wrongpassword"
        }
        response = requests.post(
            f"{test_config.base_url}/auth/login",
            json=invalid_credentials
        )
        success = response.status_code == 401  # Should fail
        test_config.add_test_result(
            "Invalid Login",
            success,
            f"Status: {response.status_code}, Expected: 401"
        )
        return success
    except Exception as e:
        test_config.add_test_result("Invalid Login", False, str(e))
        return False

def run_auth_tests():
    """Run all authentication tests"""
    print("Running Authentication Tests...")
    
    tests = [
        test_health_check,
        test_admin_login,
        test_get_current_user,
        test_user_registration,
        test_invalid_login
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"Authentication Tests: {passed}/{total} passed")
    return passed == total

if __name__ == "__main__":
    run_auth_tests() 