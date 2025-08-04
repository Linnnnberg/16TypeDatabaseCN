#!/usr/bin/env python3
"""
Script to create an admin user for testing the authentication system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal
from app.services.auth_service import AuthService
from app.database.models import UserRole

def create_admin_user(email: str, password: str, name: str):
    """Create an admin user"""
    db = SessionLocal()
    try:
        auth_service = AuthService(db)
        
        # Check if user already exists
        from app.database.models import User
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"❌ User with email {email} already exists")
            return
        
        # Create system user
        user = auth_service.create_system_user(email, password, name)
        print(f"✅ Admin user created successfully!")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Name: {user.name}")
        print(f"   Role: {user.role}")
        print(f"   Created: {user.created_at}")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Creating Admin User for 16型花名册")
    print("=" * 50)
    
    # Default admin credentials (you can change these)
    admin_email = "admin@mbti-roster.com"
    admin_password = "admin123"
    admin_name = "System Administrator"
    
    print(f"Creating admin user with:")
    print(f"  Email: {admin_email}")
    print(f"  Password: {admin_password}")
    print(f"  Name: {admin_name}")
    print()
    
    create_admin_user(admin_email, admin_password, admin_name)
    
    print("\n" + "=" * 50)
    print("📝 Next steps:")
    print("1. Start the server: python run_local.py")
    print("2. Go to http://localhost:8000/docs")
    print("3. Test the authentication endpoints:")
    print("   - POST /auth/login with admin credentials")
    print("   - GET /auth/me with the returned token")
    print("4. Create regular users via POST /auth/signup") 