from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session, selectinload

from app.models.order import Order
from app.models.orderitem import OrderItem
from app.models.productvariant import ProductVariant
from app.models.user import User
from app.models.user_address import UserAddress

from app.exceptions.order_exception import (
    UserNotFoundException,
    AddressNotFoundException,
    AddressAccessDeniedException,
    ProductVariantNotFoundException,
    InsufficientStockException,
    OrderNotFoundException,
)


class OrderRepository:

    def __init__(self, db: Session):
        self._db = db

    # ─── User / Address ───────────────────────────────────────────────────────

    def get_user_by_id(self, user_id: int) -> User:
        user = self._db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundException(f"User {user_id} not found")
        return user

    def get_default_address(self, user_id: int) -> Optional[UserAddress]:
        return (
            self._db.query(UserAddress)
            .filter(UserAddress.user_id == user_id, UserAddress.is_default == True)
            .first()
        )

    def get_address_by_id(self, address_id: int, user_id: int) -> UserAddress:
        address = self._db.query(UserAddress).filter(UserAddress.id == address_id).first()
        if not address:
            raise AddressNotFoundException(f"Address {address_id} not found")
        if address.user_id != user_id:
            raise AddressAccessDeniedException(
                f"Address {address_id} does not belong to user {user_id}"
            )
        return address

    def clear_default_address(self, user_id: int) -> None:
        (
            self._db.query(UserAddress)
            .filter(UserAddress.user_id == user_id, UserAddress.is_default == True)
            .update({"is_default": False})
        )

    def create_address(self, address: UserAddress) -> UserAddress:
        self._db.add(address)
        self._db.commit()
        self._db.refresh(address)
        return address

    # ─── Variant / Stock ──────────────────────────────────────────────────────

    def get_variant_by_id(self, variant_id: int) -> ProductVariant:
        variant = self._db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
        if not variant:
            raise ProductVariantNotFoundException(variant_id)
        return variant

    def check_stock(self, variant: ProductVariant, requested: float) -> None:
        if variant.stock_quantity < requested:
            raise InsufficientStockException(
                variant_id=variant.id,
                available=variant.stock_quantity,
                requested=requested,
            )

    # ─── Order creation ───────────────────────────────────────────────────────

    def create_order(self, order: Order) -> Order:
        try:
            self._db.add(order)
            self._db.commit()
            self._db.refresh(order)
            return order
        except:
            self._db.rollback()
            raise

    def create_order_items(self, items: List[OrderItem]) -> None:
        self._db.add_all(items)
        self._db.commit()

    # ─── Save (used after verify payment) ────────────────────────────────────

    def save(self, order: Order) -> Order:
        self._db.commit()
        self._db.refresh(order)
        return order

    # ─── Eager load options ───────────────────────────────────────────────────

    def _order_options(self):
        return [
            selectinload(Order.order_items)
                .selectinload(OrderItem.variant)
                .selectinload(ProductVariant.product)
        ]

    # ─── Fetch — user scoped ──────────────────────────────────────────────────

    def get_order_by_id(self, order_id: int, user_id: int) -> Order:
        order = (
            self._db.query(Order)
            .options(*self._order_options())
            .filter(Order.id == order_id, Order.user_id == user_id)
            .first()
        )
        if not order:
            raise OrderNotFoundException(f"Order {order_id} not found")
        return order

    def get_order_by_razorpay_order_id(self, razorpay_order_id: str, user_id: int) -> Order:
        order = (
            self._db.query(Order)
            .filter(
                Order.razorpay_order_id == razorpay_order_id,
                Order.user_id == user_id,
            )
            .first()
        )
        if not order:
            raise OrderNotFoundException(
                f"No order found for razorpay_order_id {razorpay_order_id}"
            )
        return order

    def get_my_orders_cursor(
        self,
        user_id: int,
        last_id: Optional[int],
        limit: int,
    ) -> List[Order]:
        query = (
            self._db.query(Order)
            .options(*self._order_options())
            .filter(Order.user_id == user_id)
        )
        if last_id:
            query = query.filter(Order.id < last_id)
        return query.order_by(Order.id.desc()).limit(limit + 1).all()

    # ─── Fetch — admin scoped ─────────────────────────────────────────────────

    def get_all_orders_cursor(
        self,
        last_id: Optional[int],
        limit: int,
        status: Optional[str]   = None,
        from_date               = None,
        to_date                 = None,
    ) -> List[Order]:
        query = (
            self._db.query(Order)
            .options(*self._order_options())
        )
        if status:
            query = query.filter(Order.status == status)
        if from_date:
            query = query.filter(Order.created_at >= from_date)
        if to_date:
            query = query.filter(Order.created_at <= to_date)
        if last_id:
            query = query.filter(Order.id < last_id)
        return query.order_by(Order.id.desc()).limit(limit + 1).all()

    def get_order_by_id_admin(self, order_id: int) -> Order:
        order = (
            self._db.query(Order)
            .options(*self._order_options())
            .filter(Order.id == order_id)
            .first()
        )
        if not order:
            raise OrderNotFoundException(f"Order {order_id} not found")
        return order