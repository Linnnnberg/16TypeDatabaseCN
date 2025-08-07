#!/usr/bin/env python3
"""
Browser Simulation Test
Simulates exactly what a browser does when making signup request
"""

import requests
import time
import json

def test_browser_simulation():
    base_url = "http://localhost:8000"
    
    print("Browser Simulation Test")
    print("=" * 50)
    
    # Simulate browser headers
    browser_headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Origin': 'http://localhost:8000',
        'Referer': 'http://localhost:8000/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    # Test 1: Browser health check
    print("\n1. Browser Health Check...")
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/health", headers=browser_headers, timeout=10)
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Headers: {dict(response.headers)}")
        
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test 2: Browser signup (exactly like frontend)
    print("\n2. Browser Signup Simulation...")
    try:
        test_email = f"browser_test{int(time.time())}@example.com"
        signup_data = {
            "name": "Browser Test User",
            "email": test_email,
            "password": "testpass123"
        }
        
        print(f"Signup data: {json.dumps(signup_data, indent=2)}")
        print(f"Request headers: {json.dumps(browser_headers, indent=2)}")
        
        start_time = time.time()
        response = requests.post(f"{base_url}/auth/signup", 
                               json=signup_data, 
                               headers=browser_headers,
                               timeout=10)
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("Browser signup successful!")
        else:
            print("Browser signup failed!")
            
    except requests.exceptions.Timeout:
        print("Browser signup TIMED OUT after 10 seconds!")
        print("This reproduces the frontend timeout issue!")
    except Exception as e:
        print(f"Browser signup test failed: {e}")
    
    # Test 3: Check CORS headers
    print("\n3. CORS Headers Check...")
    try:
        response = requests.options(f"{base_url}/auth/signup", headers=browser_headers)
        print(f"OPTIONS Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"CORS check failed: {e}")

if __name__ == "__main__":
    test_browser_simulation()
