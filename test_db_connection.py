#!/usr/bin/env python3
"""
Test Database Connection
Simple test to check if database operations work
"""

from app.database.database import engine, SessionLocal
from app.database.models import User, UserRole
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from sqlalchemy import text

def test_db_connection():
    """Test basic database connectivity"""
    print("Testing database connection...")
    
    try:
        # Test engine connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connection successful")
        
        # Test session creation
        db = SessionLocal()
        print("Session creation successful")
        
        # Test simple query
        user_count = db.query(User).count()
        print(f"Current user count: {user_count}")
        
        db.close()
        print("Database test completed successfully")
        return True
        
    except Exception as e:
        print(f"Database test failed: {e}")
        return False

def test_user_creation():
    """Test creating a user"""
    print("\nTesting user creation...")
    
    try:
        db = SessionLocal()
        
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("Test user already exists, deleting...")
            db.delete(existing_user)
            db.commit()
        
        # Create test user
        hashed_password = get_password_hash("test123")
        user = User(
            email="test@example.com",
            hashed_password=hashed_password,
            name="test_user",
            role=UserRole.CLIENT,
        )
        
        print("Adding user to database...")
        db.add(user)
        print("Committing transaction...")
        db.commit()
        print("Refreshing user object...")
        db.refresh(user)
        
        print(f"User created successfully with ID: {user.id}")
        
        # Clean up
        db.delete(user)
        db.commit()
        print("Test user cleaned up")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"User creation test failed: {e}")
        return False

if __name__ == "__main__":
    print("Database Connection Test")
    print("=" * 40)
    
    if test_db_connection():
        print("Database connection OK")
    else:
        print("Database connection FAILED")
        exit(1)
    
    if test_user_creation():
        print("User creation OK")
    else:
        print("User creation FAILED")
        exit(1)
    
    print("\nAll tests passed!")
