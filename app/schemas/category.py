from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Base schema (shared fields)
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url:str
    is_active: Optional[bool] = True


# Create schema
class CategoryCreate(CategoryBase):
    pass


# Update schema
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

# Response schema
class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    image_url:str

    class Config:
        from_attributes = True   # For SQLAlchemy ORM (Pydantic v2)