from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base  # your declarative base



class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False)

    description = Column(Text, nullable=True)

    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"))

    image_url = Column(String(500), nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    brand = relationship("Brand", back_populates="products")

    category = relationship("Category", back_populates="products")

    variants = relationship("ProductVariant", back_populates="product")