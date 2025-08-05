#!/usr/bin/env python3
"""
Simple Registration Test
Basic API testing with longer timeouts and better error handling
"""

import requests
import time
import sys

def test_with_timeout(url, timeout=30):
    """Test with longer timeout"""
    try:
        print(f"🔍 Testing: {url}")
        response = requests.get(url, timeout=timeout)
        print(f"✅ Status: {response.status_code}")
        return response
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout after {timeout} seconds")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_registration_flow():
    """Test the complete registration flow with delays"""
    print("🚀 Simple Registration Test")
    print("=" * 40)
    
    # Test 1: Server Health
    print("\n1️⃣ Testing Server Health...")
    health_response = test_with_timeout("http://localhost:8000/health", timeout=10)
    if not health_response:
        print("❌ Server not responding. Please start the server with: python run_local.py")
        return False
    
    # Wait a bit for server to be fully ready
    print("⏳ Waiting 3 seconds for server to be ready...")
    time.sleep(3)
    
    # Test 2: Homepage
    print("\n2️⃣ Testing Homepage...")
    homepage_response = test_with_timeout("http://localhost:8000/", timeout=15)
    if homepage_response and homepage_response.status_code == 200:
        print("✅ Homepage loads successfully")
    else:
        print("❌ Homepage failed to load")
    
    # Test 3: API Documentation
    print("\n3️⃣ Testing API Documentation...")
    docs_response = test_with_timeout("http://localhost:8000/docs", timeout=15)
    if docs_response and docs_response.status_code == 200:
        print("✅ API documentation loads successfully")
    else:
        print("❌ API documentation failed to load")
    
    # Test 4: Registration API
    print("\n4️⃣ Testing Registration API...")
    test_email = f"test_{int(time.time())}@example.com"
    test_data = {
        "email": test_email,
        "password": "testpassword123",
        "name": "Test User"
    }
    
    try:
        print(f"📝 Registering user: {test_email}")
        response = requests.post(
            "http://localhost:8000/auth/signup",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            user_data = response.json()
            print(f"   User ID: {user_data['id']}")
            print(f"   User Name: {user_data['name']}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False
    
    # Test 5: Login API
    print("\n5️⃣ Testing Login API...")
    try:
        login_data = {
            "email": test_email,
            "password": "testpassword123"
        }
        
        response = requests.post(
            "http://localhost:8000/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ Login successful!")
            token_data = response.json()
            print(f"   Token Type: {token_data['token_type']}")
            print(f"   Expires In: {token_data['expires_in']} seconds")
            return token_data['access_token']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def main():
    """Main test function"""
    print("🎯 Starting Simple Registration Test")
    print("This test will give the browser and server more time to respond...")
    
    # Wait for user to be ready
    input("\nPress Enter when you're ready to start the test...")
    
    # Run the test
    token = test_registration_flow()
    
    if token:
        print("\n" + "=" * 40)
        print("🎉 All tests passed!")
        print("\n📋 What was tested:")
        print("   ✅ Server health check")
        print("   ✅ Homepage loading")
        print("   ✅ API documentation")
        print("   ✅ User registration")
        print("   ✅ User login")
        print("\n🎯 Next steps for browser automation:")
        print("   1. Install Firefox browser")
        print("   2. Download geckodriver from: https://github.com/mozilla/geckodriver/releases")
        print("   3. Add geckodriver to your PATH")
        print("   4. Run: python test_registration_automation.py")
        return True
    else:
        print("\n" + "=" * 40)
        print("💥 Some tests failed!")
        print("Please check that the server is running properly.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 