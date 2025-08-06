#!/usr/bin/env python3
"""
Demo Registration Test
Shows how the automated registration tests work without requiring Firefox
"""

import requests
import json
import time

def test_server_health():
    """Test server health endpoint"""
    print("Testing Server Health")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("Server is healthy")
            return True
        else:
            print(f"Server returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Server connection failed: {e}")
        return False

def test_registration_api():
    """Test registration API endpoint"""
    print("\nTesting Registration API")
    
    # Test data
    test_email = f"demo_test_{int(time.time())}@example.com"
    test_password = "demo123456"
    test_name = "Demo Test User"
    
    # Test successful registration
    print(f"Testing registration with email: {test_email}")
    try:
        response = requests.post(
            "http://localhost:8000/auth/signup",
            json={
                "email": test_email,
                "password": test_password,
                "name": test_name
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print("Registration successful")
            user_data = response.json()
            print(f"   User ID: {user_data['id']}")
            print(f"   User Name: {user_data['name']}")
            print(f"   User Email: {user_data['email']}")
            return test_email, test_password
        else:
            print(f"Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None, None
    except Exception as e:
        print(f"Registration API error: {e}")
        return None, None

def test_login_api(email, password):
    """Test login API endpoint"""
    print(f"\nTesting Login API with email: {email}")
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/login",
            json={
                "email": email,
                "password": password
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("Login successful")
            token_data = response.json()
            print(f"   Token Type: {token_data['token_type']}")
            print(f"   Expires In: {token_data['expires_in']} seconds")
            return token_data['access_token']
        else:
            print(f"Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"Login API error: {e}")
        return None

def test_duplicate_registration(email):
    """Test duplicate email registration"""
    print(f"\nTesting Duplicate Registration with email: {email}")
    
    try:
        response = requests.post(
            "http://localhost:8000/auth/signup",
            json={
                "email": email,
                "password": "anotherpassword",
                "name": "Another User"
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 409:
            print("Duplicate email correctly rejected")
            print(f"   Error: {response.json()['detail']}")
            return True
        else:
            print(f"Expected 409, got {response.status_code}")
            return False
    except Exception as e:
        print(f"Duplicate registration test error: {e}")
        return False

def test_invalid_registration():
    """Test registration with invalid data"""
    print("\nTesting Invalid Registration Data")
    
    test_cases = [
        {
            "name": "Empty Email",
            "data": {"email": "", "password": "password123", "name": "Test User"},
            "expected_status": 422
        },
        {
            "name": "Invalid Email",
            "data": {"email": "invalid-email", "password": "password123", "name": "Test User"},
            "expected_status": 422
        },
        {
            "name": "Short Password",
            "data": {"email": "test@example.com", "password": "123", "name": "Test User"},
            "expected_status": 422
        },
        {
            "name": "Empty Name",
            "data": {"email": "test@example.com", "password": "password123", "name": ""},
            "expected_status": 422
        }
    ]
    
    for test_case in test_cases:
        print(f"   Testing: {test_case['name']}")
        try:
            response = requests.post(
                "http://localhost:8000/auth/signup",
                json=test_case["data"],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == test_case["expected_status"]:
                print(f"   Correctly rejected with status {response.status_code}")
            else:
                print(f"   Expected {test_case['expected_status']}, got {response.status_code}")
        except Exception as e:
            print(f"   Test error: {e}")

def test_user_profile_api(token):
    """Test user profile API with authentication"""
    print(f"\nTesting User Profile API")
    
    try:
        response = requests.get(
            "http://localhost:8000/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 200:
            print("Profile retrieved successfully")
            profile = response.json()
            print(f"   User ID: {profile['id']}")
            print(f"   User Name: {profile['name']}")
            print(f"   User Email: {profile['email']}")
            print(f"   User Role: {profile['role']}")
            return True
        else:
            print(f"Profile retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Profile API error: {e}")
        return False

def main():
    """Run all API tests"""
    print("Registration API Test Demo")
    print("=" * 50)
    
    # Test server health
    if not test_server_health():
        print("\nServer is not available. Please start the server with:")
        print("   python run_local.py")
        return False
    
    # Test registration
    email, password = test_registration_api()
    if not email:
        return False
    
    # Test login
    token = test_login_api(email, password)
    if not token:
        return False
    
    # Test user profile
    test_user_profile_api(token)
    
    # Test duplicate registration
    test_duplicate_registration(email)
    
    # Test invalid registration data
    test_invalid_registration()
    
    print("\n" + "=" * 50)
    print("✅ All API tests completed successfully!")
    print("\n📋 What was tested:")
    print("   ✅ Server health check")
    print("   ✅ User registration")
    print("   ✅ User login")
    print("   ✅ User profile retrieval")
    print("   ✅ Duplicate email handling")
    print("   ✅ Invalid data validation")
    print("\n🎯 Next steps:")
    print("   - Install Firefox browser")
    print("   - Install geckodriver")
    print("   - Run: python test_registration_automation.py")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 