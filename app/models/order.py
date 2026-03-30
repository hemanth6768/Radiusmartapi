from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    # ─── Primary key ─────────────────────────────────────────────────────────
    id = Column(Integer, primary_key=True)

    # ─── User reference ───────────────────────────────────────────────────────
    # SET NULL so order is preserved even if user is deleted
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ─── Address reference ────────────────────────────────────────────────────
    # No ondelete — address deletion is handled at app level
    address_id = Column(
        Integer,
        ForeignKey("user_addresses.id"),
        nullable=True,
    )

    # ─── Address snapshot ─────────────────────────────────────────────────────
    # Copied at order time so the order is never affected by future address edits
    customer_name    = Column(String(200), nullable=False)
    customer_email   = Column(String(200), nullable=False)
    customer_phone   = Column(String(20),  nullable=False)
    apartment_name   = Column(String(200), nullable=True)
    door_number      = Column(String(50),  nullable=True)
    customer_address = Column(Text,        nullable=False)
    city             = Column(String(100), nullable=True)
    pincode          = Column(String(20),  nullable=True)

    # ─── Order financials ─────────────────────────────────────────────────────
    total_amount = Column(Float, nullable=False)

    # ─── Order status ─────────────────────────────────────────────────────────
    # Tracks the overall order lifecycle
    # Values: pending → confirmed → shipped → delivered → cancelled
    status = Column(String(50), default="pending", nullable=False, index=True)

    # ─── Razorpay fields ──────────────────────────────────────────────────────

    # Created by your backend when calling razorpay.order.create()
    # Sent to the frontend to open the Razorpay modal
    razorpay_order_id = Column(String(100), nullable=True, unique=True, index=True)

    # Returned by Razorpay after user completes payment
    # Stored after signature verification succeeds
    razorpay_payment_id = Column(String(100), nullable=True, unique=True)

    # Tracks only the payment step — separate from order lifecycle status above
    # Values: pending → paid → failed
    payment_status = Column(String(20), nullable=True, default="pending")

    # How the user paid — sent by Razorpay in the handler response
    # Values: upi / card / netbanking / wallet / emi
    payment_method = Column(String(50), nullable=True)

    # Exact UTC timestamp when payment was confirmed and signature verified
    paid_at = Column(DateTime(timezone=True), nullable=True)

    # ─── Timestamps ───────────────────────────────────────────────────────────
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ─── Relationships ────────────────────────────────────────────────────────
    user    = relationship("User", back_populates="orders")
    address = relationship("UserAddress", back_populates="orders")

    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )