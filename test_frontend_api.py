#!/usr/bin/env python3
"""
Test Frontend API Calls
Simulates what the frontend JavaScript is doing
"""

import requests
import time
import json

def test_frontend_api_calls():
    base_url = "http://localhost:8000"
    
    print("Frontend API Call Simulation")
    print("=" * 50)
    
    # Test 1: Simulate frontend health check
    print("\n1. Testing Frontend Health Check...")
    try:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        start_time = time.time()
        response = requests.get(f"{base_url}/health", headers=headers, timeout=10)
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test 2: Simulate frontend signup (with timeout like frontend)
    print("\n2. Testing Frontend Signup (with timeout)...")
    try:
        test_email = f"frontend_test{int(time.time())}@example.com"
        signup_data = {
            "name": "Frontend Test User",
            "email": test_email,
            "password": "testpass123"
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        print(f"Signup data: {json.dumps(signup_data, indent=2)}")
        
        start_time = time.time()
        response = requests.post(f"{base_url}/auth/signup", 
                               json=signup_data, 
                               headers=headers,
                               timeout=10)  # 10 second timeout like frontend
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("Frontend signup successful!")
            
            # Test 3: Simulate frontend login
            print("\n3. Testing Frontend Login...")
            login_data = {
                "email": test_email,
                "password": "testpass123"
            }
            
            start_time = time.time()
            login_response = requests.post(f"{base_url}/auth/login", 
                                         json=login_data, 
                                         headers=headers,
                                         timeout=10)
            end_time = time.time()
            
            print(f"Login Status: {login_response.status_code}")
            print(f"Login Response time: {end_time - start_time:.2f} seconds")
            print(f"Login Response: {login_response.text}")
            
        else:
            print("Frontend signup failed!")
            
    except requests.exceptions.Timeout:
        print("Frontend signup TIMED OUT after 10 seconds!")
        print("This matches the frontend timeout issue!")
    except Exception as e:
        print(f"Frontend signup test failed: {e}")
    
    # Test 4: Check if server is responsive
    print("\n4. Server Responsiveness Check...")
    try:
        response = requests.get(f"{base_url}/api", timeout=5)
        print(f"API Status: {response.status_code}")
        print(f"API Response: {response.text}")
    except Exception as e:
        print(f"API check failed: {e}")

if __name__ == "__main__":
    test_frontend_api_calls()
