from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Tag name")
    description: Optional[str] = Field(None, description="Tag description")


class TagResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
