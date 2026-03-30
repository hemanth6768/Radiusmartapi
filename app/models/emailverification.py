from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from datetime import datetime
from app.database import Base


class EmailVerificationToken(Base):

    __tablename__ = "email_verification_tokens"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    token = Column(String(255))

    expires_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)