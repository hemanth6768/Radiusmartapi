from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.orderitem import OrderItem


class OrderRepository:

    @staticmethod
    def create_order(db: Session, order: Order):
        db.add(order)
        db.flush()  # get order.id before commit
        return order

    @staticmethod
    def create_order_item(db: Session, order_item: OrderItem):
        db.add(order_item)

    @staticmethod
    def get_by_id(db: Session, order_id: int):
        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Order).all()