from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SectionCreate(BaseModel):
    name: str
    description: Optional[str]
    image_url: Optional[str]
    display_order: Optional[int]


class SectionUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    display_order: Optional[int]
    is_active: Optional[bool]


class SectionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    image_url: Optional[str]
    display_order: Optional[int]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True