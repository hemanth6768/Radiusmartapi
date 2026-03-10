from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base  # your


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False)

    discount_type = Column(String(20), nullable=False)
    # percentage or flat

    discount_value = Column(Float, nullable=False)

    start_date = Column(DateTime)

    end_date = Column(DateTime)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    variants = relationship("ProductVariant", back_populates="offer")