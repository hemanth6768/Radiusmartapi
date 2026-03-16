from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class OfferVariant(Base):
    __tablename__ = "offer_variants"

    id = Column(Integer, primary_key=True)

    offer_id = Column(Integer, ForeignKey("offers.id"))

    variant_id = Column(Integer, ForeignKey("product_variants.id"))

    offer = relationship("Offer", back_populates="offer_variants")

    variant = relationship("ProductVariant", back_populates="offer_variants")