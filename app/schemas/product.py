from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Shared fields
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    category_id: int
    is_available: Optional[bool] = True


# Create
class ProductCreate(ProductBase):
    pass


# Update (Partial)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    category_id: Optional[int] = None
    is_available: Optional[bool] = None


# Response
class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True