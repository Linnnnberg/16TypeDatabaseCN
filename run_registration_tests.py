#!/usr/bin/env python3
"""
Registration Test Runner
Installs dependencies and runs automated registration tests
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install test dependencies"""
    print("📦 Installing test dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "selenium==4.15.2",
            "webdriver-manager==4.0.1",
            "requests==2.31.0"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_firefox():
    """Check if Firefox is available"""
    try:
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        
        # Try to initialize Firefox driver
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.quit()
        print("✅ Firefox WebDriver is available")
        return True
    except Exception as e:
        print(f"❌ Firefox WebDriver not available: {e}")
        print("Please install Firefox browser and geckodriver")
        return False

def check_server():
    """Check if the server is running"""
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print("❌ Server is not responding correctly")
            return False
    except requests.exceptions.RequestException:
        print("❌ Server is not running")
        print("Please start the server with: python run_local.py")
        return False

def run_tests():
    """Run the registration tests"""
    print("🧪 Running registration tests...")
    try:
        # Import and run tests
        from test_registration_automation import run_tests
        success = run_tests()
        return success
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Registration Test Runner")
    print("=" * 50)
    
    # Check server
    if not check_server():
        return False
    
    # Check Firefox
    if not check_firefox():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Run tests
    success = run_tests()
    
    if success:
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n💥 Some tests failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 