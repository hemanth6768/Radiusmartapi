from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum


class DiscountType(str, Enum):
    PERCENTAGE = "percentage"      # e.g. 10% off the variant price
    FLAT = "flat"                  # e.g. ₹50 off the variant price
    FIXED_PRICE = "fixed_price"    # e.g. sell at ₹199 regardless of MRP
    BUY_X_GET_Y = "buy_x_get_y"   # discount_value = free qty; use min_quantity for X


class OfferBase(BaseModel):
    name: str
    discount_type: DiscountType
    discount_value: float
    priority: int = 1
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = True

    @field_validator("discount_value")
    @classmethod
    def validate_discount_value(cls, v: float) -> float:
        if v < 0:
            raise ValueError("discount_value must be non-negative")
        return v

    @model_validator(mode="after")
    def validate_dates(self) -> "OfferBase":
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValueError("end_date must be after start_date")
        return self

    @model_validator(mode="after")
    def validate_percentage_cap(self) -> "OfferBase":
        if self.discount_type == DiscountType.PERCENTAGE and self.discount_value > 100:
            raise ValueError("Percentage discount cannot exceed 100")
        return self


class OfferCreate(OfferBase):
    variant_ids: List[int]

    @field_validator("variant_ids")
    @classmethod
    def validate_variant_ids(cls, v: List[int]) -> List[int]:
        if not v:
            raise ValueError("At least one variant_id is required")
        if len(v) != len(set(v)):
            raise ValueError("Duplicate variant_ids are not allowed")
        return v


class OfferUpdate(BaseModel):
    name: Optional[str] = None
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None

    @field_validator("discount_value")
    @classmethod
    def validate_discount_value(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("discount_value must be non-negative")
        return v


class OfferVariantResponse(BaseModel):
    id: int
    variant_id: int

    class Config:
        from_attributes = True


class OfferResponse(OfferBase):
    id: int
    created_at: Optional[datetime] = None
    offer_variants: List[OfferVariantResponse] = []

    class Config:
        from_attributes = True


class VariantOfferResponse(BaseModel):
    """Which offer(s) are active for a given variant."""
    variant_id: int
    offers: List[OfferResponse]