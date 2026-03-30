from sqlalchemy import Column, Integer, ForeignKey , String , DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base



class AuthAuditLog(Base):

    __tablename__ = "auth_audit_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    action = Column(String(100))

    ip_address = Column(String)

    user_agent = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)