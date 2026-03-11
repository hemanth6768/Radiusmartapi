from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# -------------------------
# Brand Schema (for response)
# -------------------------

class BrandResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# -------------------------
# Category Schema (optional but useful)
# -------------------------

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# -------------------------
# Variant Schemas
# -------------------------

class VariantBase(BaseModel):
    pricing_model: str
    base_unit: str
    value: Optional[float] = None
    base_price: float
    stock_quantity: float
    image_url: Optional[str] = None
    offer_id: Optional[int] = None


class VariantCreate(VariantBase):
    pass


class VariantUpdate(BaseModel):
    pricing_model: Optional[str] = None
    base_unit: Optional[str] = None
    value: Optional[float] = None
    base_price: Optional[float] = None
    stock_quantity: Optional[float] = None
    image_url: Optional[str] = None
    offer_id: Optional[int] = None


class VariantResponse(VariantBase):
    id: int

    class Config:
        from_attributes = True


# -------------------------
# Product Schemas
# -------------------------

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    brand_id: Optional[int] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = True


class ProductCreate(ProductBase):
    variants: List[VariantCreate]


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    image_url: Optional[str]
    is_active: bool
    created_at: datetime

    brand: Optional[BrandResponse]
    category: Optional[CategoryResponse]

    variants: List[VariantResponse] = []

    class Config:
        from_attributes = True
