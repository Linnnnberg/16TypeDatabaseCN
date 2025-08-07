#!/usr/bin/env python3
"""
Debug Authentication Issue
Test the authentication endpoints to identify the problem
"""

import requests
import json

def test_signup():
    """Test the signup endpoint"""
    url = "http://localhost:8000/auth/signup"
    data = {
        "name": "test_user",
        "email": "test@example.com",
        "password": "test123"
    }
    
    print("Testing signup endpoint...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 201:
            print("Signup successful!")
            return response.json()
        else:
            print("Signup failed!")
            return None
            
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_login():
    """Test the login endpoint"""
    url = "http://localhost:8000/auth/login"
    data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    print("\nTesting login endpoint...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("Login successful!")
            return response.json()
        else:
            print("Login failed!")
            return None
            
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_health():
    """Test if the server is running"""
    url = "http://localhost:8000/health"
    
    print("Testing server health...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("Server is running!")
            return True
        else:
            print("Server health check failed!")
            return False
            
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    print("Debugging Authentication Issue")
    print("=" * 50)
    
    # Test server health first
    if not test_health():
        print("Server is not running or not accessible!")
        exit(1)
    
    # Test signup
    signup_result = test_signup()
    
    # Test login
    login_result = test_login()
    
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"Server Health: {'OK' if test_health() else 'Failed'}")
    print(f"Signup: {'OK' if signup_result else 'Failed'}")
    print(f"Login: {'OK' if login_result else 'Failed'}")
