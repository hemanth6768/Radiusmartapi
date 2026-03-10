from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BrandBase(BaseModel):
    name: str
    logo_url: Optional[str] = None
    description: Optional[str] = None


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None


class BrandResponse(BrandBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True