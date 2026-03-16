from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class RolePermission(Base):

    __tablename__ = "role_permissions"

    id = Column(BigInteger, primary_key=True)

    role_id = Column(BigInteger, ForeignKey("roles.id"))

    permission_id = Column(BigInteger, ForeignKey("permissions.id"))

    role = relationship("Role", back_populates="permissions")

    permission = relationship("Permission")