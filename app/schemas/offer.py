from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OfferBase(BaseModel):
    name: str
    discount_type: str
    discount_value: float
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = True


class OfferCreate(OfferBase):
    pass


class OfferUpdate(BaseModel):
    name: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None


class OfferResponse(OfferBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True