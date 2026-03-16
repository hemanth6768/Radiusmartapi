from sqlalchemy import Column, BigInteger, ForeignKey, String, Boolean, DateTime
from datetime import datetime
from app.database import Base


class Session(Base):

    __tablename__ = "sessions"

    id = Column(BigInteger, primary_key=True)

    user_id = Column(BigInteger, ForeignKey("users.id"))

    refresh_token = Column(String)

    device_info = Column(String)

    ip_address = Column(String)

    expires_at = Column(DateTime)

    revoked = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)