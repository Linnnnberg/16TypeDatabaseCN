#!/usr/bin/env python3
"""
Test Configuration Script
Verify that settings are loaded correctly
"""

import os
import sys

def test_config():
    """Test that the configuration loads correctly"""
    print("=== Testing Configuration ===")
    
    # Set CI environment if not already set
    if not os.getenv("CI"):
        os.environ["CI"] = "true"
        print("Set CI=true")
    
    # Set required environment variables
    os.environ["DATABASE_URL"] = "sqlite:///./test_mbti_roster.db"
    os.environ["SECRET_KEY"] = "test-secret-key-for-ci-12345"
    
    try:
        # Import settings after environment is set
        from app.core.config import settings
        
        print("SUCCESS: Settings imported successfully")
        print(f"Database URL: {settings.database_url}")
        print(f"Secret Key: {settings.secret_key[:20]}...")
        print(f"Redis URL: {settings.redis_url}")
        print(f"Email From: {settings.email_from}")
        print(f"Daily Vote Limit: {settings.daily_vote_limit}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to load settings: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n=== Testing Database Connection ===")
    
    try:
        from app.database.database import create_tables
        
        create_tables()
        print("SUCCESS: Database tables created successfully")
        return True
        
    except Exception as e:
        print(f"ERROR: Database connection failed: {e}")
        return False

def main():
    """Main test function"""
    print("Configuration Test Script")
    print("=" * 40)
    
    # Test configuration loading
    config_ok = test_config()
    
    # Test database connection
    db_ok = test_database_connection()
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Configuration: {'PASS' if config_ok else 'FAIL'}")
    print(f"Database: {'PASS' if db_ok else 'FAIL'}")
    
    if config_ok and db_ok:
        print("SUCCESS: All tests passed!")
        return 0
    else:
        print("FAILED: Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 