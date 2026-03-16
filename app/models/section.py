from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True)

    name = Column(String(200), nullable=False, unique=True)

    description = Column(Text, nullable=True)

    image_url = Column(String(500), nullable=True)

    display_order = Column(Integer, nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    categories = relationship("Category", back_populates="section")