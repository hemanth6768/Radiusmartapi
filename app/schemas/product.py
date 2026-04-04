from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import datetime


# -------------------------
# Brand Schema
# -------------------------

class BrandResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# -------------------------
# Category Schema
# -------------------------

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# -------------------------
# Offer Schema
# -------------------------

class OfferResponse(BaseModel):
    id: int
    name: str
    discount_type: str
    discount_value: float

    class Config:
        from_attributes = True


# -------------------------
# OfferVariant Schema (join table — internal only)
# -------------------------

class OfferVariantResponse(BaseModel):
    offer: OfferResponse

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
    sales_price: Optional[float] = None


# Used when creating product variants
class VariantCreate(VariantBase):
    pass


# Used when updating variant details
class VariantUpdate(BaseModel):
    pricing_model: Optional[str] = None
    base_unit: Optional[str] = None
    value: Optional[float] = None
    base_price: Optional[float] = None
    sales_price: Optional[float] = None      # ← add this, it was missing
    stock_quantity: Optional[float] = None
    image_url: Optional[str] = None


# Variant returned in API responses
class VariantResponse(VariantBase):
    id: int

    # Field(exclude=True) — read from DB for flattening but never sent in response
    offer_variants: List[OfferVariantResponse] = Field(default=[], exclude=True)

    # Clean flattened offers list — this is what the UI receives
    offers: List[OfferResponse] = []

    @model_validator(mode="after")
    def flatten_offers(self) -> "VariantResponse":
        if self.offer_variants:
            self.offers = [ov.offer for ov in self.offer_variants]
        return self

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
    is_active: Optional[bool] = True


# Used when creating a product
# Variants are created along with the product
class ProductCreate(ProductBase):
    variants: List[VariantCreate]


# Used when updating product details
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


# Product returned in API responses
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