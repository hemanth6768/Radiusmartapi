from sqlalchemy import Column, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class UserRole(Base):

    __tablename__ = "user_roles"

    id = Column(BigInteger, primary_key=True)

    user_id = Column(BigInteger, ForeignKey("users.id"))

    role_id = Column(BigInteger, ForeignKey("roles.id"))

    assigned_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="roles")