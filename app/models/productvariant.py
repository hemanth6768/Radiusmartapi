from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id"))

    pricing_model = Column(String(20), nullable=False)
    # weight or fixed

    base_unit = Column(String(20), nullable=False)
    # kg, g, ml, liter, piece, pack

    base_price = Column(Float, nullable=False)

    value = Column(Float, nullable=True)
    # used for fixed products (500ml, 1kg etc)
    image_url = Column(String(500), nullable=True)
       #
    stock_quantity = Column(Float, default=0)

    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=True)

    product = relationship("Product", back_populates="variants")

    order_items = relationship("OrderItem", back_populates="variant")

    offer = relationship("Offer", back_populates="variants")