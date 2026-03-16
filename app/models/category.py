from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)

    name = Column(String(200), nullable=False, unique=True)

    description = Column(Text, nullable=True)

    image_url = Column(String(500), nullable=True)

    section_id = Column(Integer, ForeignKey("sections.id") , index = True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    section = relationship("Section", back_populates="categories")

    products = relationship("Product", back_populates="category")