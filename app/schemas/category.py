from pydantic import BaseModel
from typing import Optional , List
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    section_id: Optional[int] = None
    is_active: Optional[bool] = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    section_id: Optional[int] = None
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SectionWithCategories(BaseModel):
    id: int
    name: str
    image_url: str | None = None
    display_order: int
    is_active: bool
    categories: List[CategoryResponse]

    class Config:
        from_attributes = True
