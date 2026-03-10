from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.Repository.order_repository import OrderRepository
from app.models.order import Order
from app.models.orderitem import OrderItem
from app.models.productvariant import ProductVariant
from app.schemas.order import OrderCreate


class OrderService:


    @staticmethod
    def create_order(db: Session, order_data: OrderCreate):

        total_amount = 0

        order_items = []

        for item in order_data.items:

            variant = db.query(ProductVariant).filter(
                ProductVariant.id == item.variant_id
            ).first()

            if not variant:
                raise HTTPException(404, "Variant not found")

            price = variant.base_price

            # Apply offer if exists
            if variant.offer:

                if variant.offer.discount_type == "flat":
                    price -= variant.offer.discount_value

                elif variant.offer.discount_type == "percentage":
                    price -= price * variant.offer.discount_value / 100

            item_total = price * item.quantity

            total_amount += item_total

            order_items.append(
                OrderItem(
                    variant_id=item.variant_id,
                    quantity=item.quantity,
                    price_per_unit=price,
                    total_price=item_total
                )
            )


        order = Order(
            customer_name=order_data.customer_name,
            customer_email=order_data.customer_email,
            customer_phone=order_data.customer_phone,
            apartment_name=order_data.apartment_name,
            door_number=order_data.door_number,
            customer_address=order_data.customer_address,
            total_amount=total_amount,
            order_items=order_items
        )

        return OrderRepository.create_order(db, order)


    @staticmethod
    def get_orders(db: Session):
        return OrderRepository.get_orders(db)


    @staticmethod
    def get_order(db: Session, order_id: int):

        order = OrderRepository.get_order_by_id(db, order_id)

        if not order:
            raise HTTPException(404, "Order not found")

        return order