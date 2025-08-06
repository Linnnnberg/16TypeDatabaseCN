from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.database.models import User
from app.schemas.user import UserUpdate, UserProfile


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_profile(self, user_id: str) -> UserProfile:
        """Get user profile"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return UserProfile.model_validate(user)

    def update_user(self, user_id: str, user_data: UserUpdate) -> UserProfile:
        """Update user information"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Update fields if provided
        if user_data.name is not None:
            user.name = user_data.name
        if user_data.is_active is not None:
            user.is_active = user_data.is_active

        self.db.commit()
        self.db.refresh(user)

        return UserProfile.model_validate(user)

    def deactivate_user(self, user_id: str) -> UserProfile:
        """Deactivate user account"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        user.is_active = False
        self.db.commit()
        self.db.refresh(user)

        return UserProfile.model_validate(user)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return self.db.query(User).offset(skip).limit(limit).all()
