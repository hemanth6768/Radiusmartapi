from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ─────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────

class OrderStatus(str, Enum):
    PENDING   = "pending"
    CONFIRMED = "confirmed"
    SHIPPED   = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID    = "paid"
    FAILED  = "failed"


# ─────────────────────────────────────────────
# CHECKOUT PREFILL
# ─────────────────────────────────────────────

class CheckoutPrefillResponse(BaseModel):
    has_default:    bool
    address_id:     Optional[int] = None
    customer_name:  Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    apartment_name: Optional[str] = None
    door_number:    Optional[str] = None
    address:        Optional[str] = None
    city:           Optional[str] = None
    pincode:        Optional[str] = None
    label:          Optional[str] = None


# ─────────────────────────────────────────────
# ORDER ITEM — compact (used in list view)
# ─────────────────────────────────────────────

class OrderItemSummary(BaseModel):
    variant_id:    int
    product_name:  Optional[str]  = None
    base_unit:     Optional[str]  = None
    value:         Optional[float] = None
    quantity:      float
    final_price:   float
    variant_image: Optional[str]  = None

    model_config = {"from_attributes": True}

    @classmethod
    def from_order_item(cls, item) -> "OrderItemSummary":
        variant = item.variant
        product = variant.product if variant else None
        return cls(
            variant_id=item.variant_id,
            product_name=product.name if product else None,
            base_unit=variant.base_unit if variant else None,
            value=variant.value if variant else None,
            quantity=item.quantity,
            final_price=item.final_price,
            variant_image=(
                f"/static/{variant.image_url}"
                if variant and variant.image_url
                else None
            ),
        )


# ─────────────────────────────────────────────
# ORDER ITEM — full (used in detail view)
# ─────────────────────────────────────────────

class OrderItemOut(BaseModel):
    variant_id:      int
    quantity:        float
    unit_price:      float
    discount_amount: float
    final_price:     float
    product_name:    Optional[str]  = None
    base_unit:       Optional[str]  = None
    value:           Optional[float] = None
    variant_image:   Optional[str]  = None

    model_config = {"from_attributes": True}

    @classmethod
    def from_order_item(cls, item) -> "OrderItemOut":
        variant = item.variant
        product = variant.product if variant else None
        return cls(
            variant_id=item.variant_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount_amount=item.discount_amount,
            final_price=item.final_price,
            product_name=product.name if product else None,
            base_unit=variant.base_unit if variant else None,
            value=variant.value if variant else None,
            variant_image=(
                f"/static/{variant.image_url}"
                if variant and variant.image_url
                else None
            ),
        )


# ─────────────────────────────────────────────
# PLACE ORDER — REQUEST
# ─────────────────────────────────────────────

class OrderItemIn(BaseModel):
    variant_id: int   = Field(..., gt=0)
    quantity:   float = Field(..., gt=0)


class PlaceOrderRequest(BaseModel):
    use_address_id:   Optional[int] = Field(None, gt=0)
    customer_name:    Optional[str] = Field(None, max_length=200)
    customer_phone:   Optional[str] = Field(None, max_length=20)
    customer_email:   Optional[str] = Field(None, max_length=200)
    apartment_name:   Optional[str] = Field(None, max_length=200)
    door_number:      Optional[str] = Field(None, max_length=50)
    customer_address: Optional[str] = None
    city:             Optional[str] = Field(None, max_length=100)
    pincode:          Optional[str] = Field(None, max_length=20)
    save_as_default:  bool          = False
    items:            List[OrderItemIn] = Field(..., min_length=1)

    def is_manual_entry(self) -> bool:
        return self.use_address_id is None

    def missing_manual_fields(self) -> List[str]:
        required = {
            "customer_name":    self.customer_name,
            "customer_phone":   self.customer_phone,
            "customer_email":   self.customer_email,
            "customer_address": self.customer_address,
            "city":             self.city,
            "pincode":          self.pincode,
        }
        return [k for k, v in required.items() if not v]


# ─────────────────────────────────────────────
# PLACE ORDER — RESPONSE  (now includes razorpay fields)
# ─────────────────────────────────────────────

class PlaceOrderResponse(BaseModel):
    order_id:           int
    status:             OrderStatus
    payment_status:     PaymentStatus
    total_amount:       float
    customer_name:      str
    customer_email:     str
    customer_phone:     str
    customer_address:   str
    city:               str
    pincode:            str
    items:              List[OrderItemOut]

    # Razorpay — frontend needs these to open the modal
    razorpay_order_id:  str
    razorpay_key:       str          # public key, safe to expose

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────
# VERIFY PAYMENT — REQUEST & RESPONSE
# ─────────────────────────────────────────────

class VerifyPaymentRequest(BaseModel):
    razorpay_order_id:   str = Field(..., min_length=1)
    razorpay_payment_id: str = Field(..., min_length=1)
    razorpay_signature:  str = Field(..., min_length=1)
    payment_method:      Optional[str] = None   # upi / card / netbanking — sent by frontend


class VerifyPaymentResponse(BaseModel):
    success:        bool
    order_id:       int
    status:         OrderStatus
    payment_status: PaymentStatus
    paid_at:        Optional[datetime] = None


# ─────────────────────────────────────────────
# ORDER LIST — compact card
# ─────────────────────────────────────────────

class OrderListResponse(BaseModel):
    id:               int
    status:           OrderStatus
    payment_status:   Optional[PaymentStatus] = None
    total_amount:     float
    created_at:       datetime
    item_count:       int          = 0
    customer_name:    str
    customer_phone:   str
    customer_email:   str
    apartment_name:   Optional[str] = None
    door_number:      Optional[str] = None
    customer_address: str
    city:             str
    pincode:          str
    items:            List[OrderItemSummary] = []

    model_config = {"from_attributes": True}

    @classmethod
    def from_order(cls, order) -> "OrderListResponse":
        return cls(
            id=order.id,
            status=order.status,
            payment_status=order.payment_status,
            total_amount=order.total_amount,
            created_at=order.created_at,
            item_count=len(order.order_items),
            customer_name=order.customer_name,
            customer_phone=order.customer_phone,
            customer_email=order.customer_email,
            apartment_name=order.apartment_name,
            door_number=order.door_number,
            customer_address=order.customer_address,
            city=order.city,
            pincode=order.pincode,
            items=[OrderItemSummary.from_order_item(i) for i in order.order_items],
        )


# ─────────────────────────────────────────────
# ORDER DETAIL — full view
# ─────────────────────────────────────────────

class OrderDetailResponse(BaseModel):
    id:                  int
    status:              OrderStatus
    payment_status:      Optional[PaymentStatus] = None
    payment_method:      Optional[str]           = None
    total_amount:        float
    created_at:          datetime
    paid_at:             Optional[datetime]       = None
    razorpay_order_id:   Optional[str]           = None
    razorpay_payment_id: Optional[str]           = None
    customer_name:       str
    customer_email:      str
    customer_phone:      str
    apartment_name:      Optional[str]           = None
    door_number:         Optional[str]           = None
    customer_address:    str
    city:                str
    pincode:             str
    items:               List[OrderItemOut]      = []

    model_config = {"from_attributes": True}

    @classmethod
    def from_order(cls, order) -> "OrderDetailResponse":
        return cls(
            id=order.id,
            status=order.status,
            payment_status=order.payment_status,
            payment_method=order.payment_method,
            total_amount=order.total_amount,
            created_at=order.created_at,
            paid_at=order.paid_at,
            razorpay_order_id=order.razorpay_order_id,
            razorpay_payment_id=order.razorpay_payment_id,
            customer_name=order.customer_name,
            customer_email=order.customer_email,
            customer_phone=order.customer_phone,
            apartment_name=order.apartment_name,
            door_number=order.door_number,
            customer_address=order.customer_address,
            city=order.city,
            pincode=order.pincode,
            items=[OrderItemOut.from_order_item(i) for i in order.order_items],
        )