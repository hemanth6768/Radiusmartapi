from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    variant_id = Column(Integer, ForeignKey("product_variants.id"))

    quantity = Column(Float, nullable=False)

    unit_price = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0)
    final_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_items")
    variant = relationship("ProductVariant")