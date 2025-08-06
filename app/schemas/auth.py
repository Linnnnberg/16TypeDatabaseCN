from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.database.models import UserRole


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ..., min_length=6, description="User's password (minimum 6 characters)"
    )
    name: str = Field(
        ..., min_length=1, max_length=100, description="User's display name"
    )


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
