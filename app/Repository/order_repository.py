from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.orderitem import OrderItem


class OrderRepository:

    @staticmethod
    def create_order(db: Session, order: Order):

        db.add(order)
        db.commit()
        db.refresh(order)

        return order


    @staticmethod
    def get_orders(db: Session):
        return db.query(Order).all()


    @staticmethod
    def get_order_by_id(db: Session, order_id: int):
        return db.query(Order).filter(Order.id == order_id).first()