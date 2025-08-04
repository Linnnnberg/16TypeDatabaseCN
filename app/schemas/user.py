from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.database.models import UserRole

class UserProfile(BaseModel):
    id: str
    email: str
    name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="User's display name")
    is_active: Optional[bool] = None 