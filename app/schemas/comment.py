from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CommentCreate(BaseModel):
    celebrity_id: str = Field(..., description="ID of the celebrity to comment on")
    content: str = Field(
        ..., min_length=1, max_length=1000, description="Comment content"
    )
    parent_id: Optional[str] = Field(
        None, description="ID of parent comment for replies"
    )


class CommentResponse(BaseModel):
    id: str
    user_id: str
    celebrity_id: str
    content: str
    parent_id: Optional[str] = None
    level: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
