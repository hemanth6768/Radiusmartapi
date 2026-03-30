from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True)

    product_id = Column(Integer, ForeignKey("products.id"))

    pricing_model = Column(String(20), nullable=False)

    base_unit = Column(String(20), nullable=False)

    base_price = Column(Float, nullable=False)

    sales_price = Column(Float, nullable=True)

    value = Column(Float, nullable=True)

    image_url = Column(String(500), nullable=True)

    stock_quantity = Column(Float, default=0)

    product = relationship("Product", back_populates="variants")

    order_items = relationship("OrderItem", back_populates="variant")

    offer_variants = relationship("OfferVariant", back_populates="variant")