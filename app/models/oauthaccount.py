from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from datetime import datetime
from app.database import Base


class OAuthAccount(Base):

    __tablename__ = "oauth_accounts"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    provider = Column(String(50))

    provider_user_id = Column(String(255))

    access_token = Column(String)

    refresh_token = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)