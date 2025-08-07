#!/usr/bin/env python3
"""
Detailed Authentication Debug Script
"""

import requests
import time
import json

def test_auth_detailed():
    base_url = "http://localhost:8000"
    
    print("Detailed Authentication Test")
    print("=" * 50)
    
    # Test 1: Health endpoint
    print("\n1. Testing Health Endpoint...")
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/health", timeout=5)
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Health test failed: {e}")
        return
    
    # Test 2: Auth endpoint without data
    print("\n2. Testing Auth Endpoint (no data)...")
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/auth/signup", 
                               json={"invalid": "data"}, 
                               timeout=10)
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Auth test failed: {e}")
    
    # Test 3: Valid signup
    print("\n3. Testing Valid Signup...")
    try:
        test_email = f"test{int(time.time())}@example.com"
        signup_data = {
            "name": "Test User",
            "email": test_email,
            "password": "testpass123"
        }
        
        print(f"Signup data: {json.dumps(signup_data, indent=2)}")
        
        start_time = time.time()
        response = requests.post(f"{base_url}/auth/signup", 
                               json=signup_data, 
                               timeout=10)
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("Signup successful!")
            
            # Test 4: Login with the same credentials
            print("\n4. Testing Login...")
            login_data = {
                "email": test_email,
                "password": "testpass123"
            }
            
            start_time = time.time()
            login_response = requests.post(f"{base_url}/auth/login", 
                                         json=login_data, 
                                         timeout=10)
            end_time = time.time()
            
            print(f"Login Status: {login_response.status_code}")
            print(f"Login Response time: {end_time - start_time:.2f} seconds")
            print(f"Login Response: {login_response.text}")
            
        else:
            print("Signup failed!")
            
    except Exception as e:
        print(f"Valid signup test failed: {e}")
    
    # Test 5: Check server logs
    print("\n5. Server Status Check...")
    try:
        response = requests.get(f"{base_url}/api", timeout=5)
        print(f"API Status: {response.status_code}")
        print(f"API Response: {response.text}")
    except Exception as e:
        print(f"API check failed: {e}")

if __name__ == "__main__":
    test_auth_detailed()
