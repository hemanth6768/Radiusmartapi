from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemCreate(BaseModel):
    variant_id: int
    quantity: float


class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str
    apartment_name: Optional[str] = None
    door_number: Optional[str] = None
    customer_address: str

    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    variant_id: int
    quantity: float
    price_per_unit: float
    total_price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    total_amount: float
    status: str
    created_at: datetime
    order_items: List[OrderItemResponse]

    class Config:
        from_attributes = True