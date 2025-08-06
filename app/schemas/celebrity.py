from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CelebrityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Celebrity's name")
    name_en: Optional[str] = Field(
        None, max_length=200, description="Celebrity's English name"
    )
    description: Optional[str] = Field(None, description="Celebrity's description")
    image_url: Optional[str] = Field(None, description="Celebrity's image URL")


class CelebrityUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Celebrity's name"
    )
    name_en: Optional[str] = Field(
        None, max_length=200, description="Celebrity's English name"
    )
    description: Optional[str] = Field(None, description="Celebrity's description")
    image_url: Optional[str] = Field(None, description="Celebrity's image URL")


class CelebrityResponse(BaseModel):
    id: str
    name: str
    name_en: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
