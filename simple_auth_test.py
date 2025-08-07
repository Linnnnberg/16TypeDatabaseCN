#!/usr/bin/env python3
"""
Simple Authentication Test
Test basic connectivity and identify where the issue occurs
"""

import requests
import time

def test_basic_connectivity():
    """Test basic server connectivity"""
    print("Testing basic connectivity...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"Health endpoint: {response.status_code}")
        
        # Test API root
        response = requests.get("http://localhost:8000/api", timeout=5)
        print(f"API root: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"Connectivity test failed: {e}")
        return False

def test_auth_endpoint_response():
    """Test if auth endpoint responds at all"""
    print("\nTesting auth endpoint response...")
    
    try:
        # Test with invalid data to see if endpoint responds
        response = requests.post(
            "http://localhost:8000/auth/signup",
            json={"invalid": "data"},
            timeout=10
        )
        print(f"Auth endpoint responded: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return True
    except requests.exceptions.Timeout:
        print("Auth endpoint timed out - server is hanging!")
        return False
    except Exception as e:
        print(f"Auth endpoint error: {e}")
        return False

def test_valid_signup():
    """Test valid signup data"""
    print("\nTesting valid signup...")
    
    data = {
        "name": "test_user",
        "email": "test@example.com", 
        "password": "test123"
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/auth/signup",
            json=data,
            timeout=15
        )
        end_time = time.time()
        
        print(f"Request completed in {end_time - start_time:.2f} seconds")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        return response.status_code == 201
    except requests.exceptions.Timeout:
        print("Signup request timed out!")
        return False
    except Exception as e:
        print(f"Signup error: {e}")
        return False

if __name__ == "__main__":
    print("Simple Authentication Test")
    print("=" * 40)
    
    # Test 1: Basic connectivity
    if not test_basic_connectivity():
        print("Basic connectivity failed!")
        exit(1)
    
    # Test 2: Auth endpoint response
    if not test_auth_endpoint_response():
        print("Auth endpoint not responding!")
        exit(1)
    
    # Test 3: Valid signup
    if test_valid_signup():
        print("Signup working correctly!")
    else:
        print("Signup failed!")
    
    print("\n" + "=" * 40)
    print("Test completed!")
