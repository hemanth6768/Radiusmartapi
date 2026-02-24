from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.order import Order
from app.models.orderitem import OrderItem
from app.models.product import Product
from app.Repository.order_repository import OrderRepository
from app.schemas.order import OrderCreate


class OrderService:

    @staticmethod
    def create_order(db: Session, order_data: OrderCreate):

        total_amount = 0
        order_items_objects = []

        # Validate products & calculate total
        for item in order_data.items:

            product = db.query(Product).filter(Product.id == item.product_id).first()

            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

            if product.stock_quantity < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")

            item_total = product.price * item.quantity
            total_amount += item_total

            order_item = OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                price_per_unit=product.price,
                total_price=item_total
            )

            order_items_objects.append(order_item)

            # Reduce stock
            product.stock_quantity -= item.quantity

        # Create order
        db_order = Order(
            customer_name=order_data.customer_name,
            customer_email=order_data.customer_email,
            customer_phone=order_data.customer_phone,
            customer_address=order_data.customer_address,
            total_amount=total_amount,
            status="pending"
        )

        OrderRepository.create_order(db, db_order)

        # Attach order items
        for order_item in order_items_objects:
            order_item.order_id = db_order.id
            OrderRepository.create_order_item(db, order_item)

        db.commit()
        db.refresh(db_order)

        return db_order

    @staticmethod
    def get_orders(db: Session):
        return OrderRepository.get_all(db)

    @staticmethod
    def get_order(db: Session, order_id: int):
        order = OrderRepository.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order