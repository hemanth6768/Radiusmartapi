from pydantic import BaseModel, Field, model_validator
from typing import List, Optional


# -------------------------
# Offer Schema
# -------------------------

class OfferPreview(BaseModel):
    id: int
    name: str
    discount_type: str
    discount_value: float

    class Config:
        from_attributes = True


# -------------------------
# OfferVariant (join table — internal only)
# -------------------------

class OfferVariantPreview(BaseModel):
    offer: OfferPreview

    class Config:
        from_attributes = True


# -------------------------
# Variant Preview
# -------------------------

class VariantPreview(BaseModel):
    id: int
    base_unit: str
    value: Optional[float]
    base_price: float
    sales_price: Optional[float] = None
    stock_quantity: float
    image_url: Optional[str]

    # Field(exclude=True) — read from DB for flattening but never sent in response
    offer_variants: List[OfferVariantPreview] = Field(default=[], exclude=True)

    # Clean flattened offers list — this is what the UI receives
    offers: List[OfferPreview] = []

    @model_validator(mode="after")
    def flatten_offers(self) -> "VariantPreview":
        if self.offer_variants:
            self.offers = [ov.offer for ov in self.offer_variants]
        return self

    class Config:
        from_attributes = True


# -------------------------
# Product Preview
# -------------------------

class ProductPreview(BaseModel):
    id: int
    name: str
    image_url: Optional[str]
    variants: List[VariantPreview]

    class Config:
        from_attributes = True


# -------------------------
# Category with Products
# -------------------------

class CategoryWithProducts(BaseModel):
    id: int
    name: str
    next_cursor: Optional[str]
    products: List[ProductPreview]

    class Config:
        from_attributes = True


# -------------------------
# Section with Categories
# -------------------------

class SectionWithCategories(BaseModel):
    id: int
    name: str
    categories: List[CategoryWithProducts]

    class Config:
        from_attributes = True


# -------------------------
# Home Response
# -------------------------

class HomeResponse(BaseModel):
    sections: List[SectionWithCategories]