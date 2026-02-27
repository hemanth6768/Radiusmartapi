from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base  # your declarative base




class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String(200), nullable=False)
    customer_email = Column(String(200), nullable=False)
    customer_phone = Column(String(20), nullable=False)

    # 🔥 New structured address fields
    apartment_name = Column(String(200), nullable=True)
    door_number = Column(String(50), nullable=True)

    customer_address = Column(Text, nullable=False)  
    # Street, landmark, area etc.

    total_amount = Column(Float, nullable=False)

    status = Column(String(50), default="pending")
    # pending, confirmed, shipped, delivered, cancelled

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete")