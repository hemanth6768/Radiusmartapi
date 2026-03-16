from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base  # your declara




class Brand(Base):
    
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)

    name = Column(String(200), nullable=False, unique=True)

    logo_url = Column(String(500), nullable=True)

    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    products = relationship("Product", back_populates="brand")