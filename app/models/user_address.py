from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class UserAddress(Base):
    __tablename__ = "user_addresses"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Optional label for UI
    label = Column(String(50), nullable=True)  
    # Example: "Home", "Office"

    # Contact details (can differ from user profile)
    customer_name = Column(String(200), nullable=False)
    customer_phone = Column(String(20), nullable=False)

    # Address fields
    apartment_name = Column(String(200), nullable=True)
    door_number = Column(String(50), nullable=True)

    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    pincode = Column(String(20), nullable=False)

    # Default address for checkout
    is_default = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # ================= RELATIONSHIPS =================

    user = relationship("User", back_populates="addresses")

    orders = relationship(
        "Order",
        back_populates="address"
        # ❗ DO NOT cascade delete
        # Orders must survive even if address is deleted
    )