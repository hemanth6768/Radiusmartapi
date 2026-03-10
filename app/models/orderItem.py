from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))

    variant_id = Column(Integer, ForeignKey("product_variants.id"))

    quantity = Column(Float, nullable=False)

    unit = Column(String(20), nullable=True)

    price_per_unit = Column(Float, nullable=False)

    total_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_items")

    variant = relationship("ProductVariant", back_populates="order_items")