from sqlalchemy import Column, BigInteger, ForeignKey, String, DateTime
from datetime import datetime
from app.database import Base


class EmailVerificationToken(Base):

    __tablename__ = "email_verification_tokens"

    id = Column(BigInteger, primary_key=True)

    user_id = Column(BigInteger, ForeignKey("users.id"))

    token = Column(String(255))

    expires_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)