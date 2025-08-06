from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.database.models import MBTIType


class VoteCreate(BaseModel):
    celebrity_id: str = Field(..., description="ID of the celebrity to vote for")
    mbti_type: MBTIType = Field(..., description="MBTI personality type")
    reason: Optional[str] = Field(None, description="Reason for the vote")


class VoteResponse(BaseModel):
    id: str
    user_id: str
    celebrity_id: str
    mbti_type: MBTIType
    reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
