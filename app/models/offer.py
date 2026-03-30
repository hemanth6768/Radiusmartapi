from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)

    name = Column(String(200), nullable=False , index = True)

    discount_type = Column(String(20), nullable=False)
    # percentage or flat

    discount_value = Column(Float, nullable=False)

    priority = Column(Integer, default=1, index=True)

    start_date = Column(DateTime)

    end_date = Column(DateTime)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    offer_variants = relationship("OfferVariant", back_populates="offer")