from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# ===== Order Item Create =====
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


# ===== Order Create =====
class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str

    apartment_name: Optional[str] = None
    door_number: Optional[str] = None

    customer_address: str

    items: List[OrderItemCreate]

# ===== Order Item Response =====
class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_per_unit: float
    total_price: float

    class Config:
        from_attributes = True


# ===== Order Response =====
class OrderResponse(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    customer_phone: str

    apartment_name: Optional[str]
    door_number: Optional[str]

    customer_address: str
    total_amount: float
    status: str
    created_at: datetime
    order_items: List[OrderItemResponse]

    class Config:
        from_attributes = True