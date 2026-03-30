from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order
import qrcode
import base64
from io import BytesIO

router = APIRouter(prefix="/payment", tags=["Payment"])

UPI_ID = "9449436768-2@axl"       # 🔹 Fill this
STORE_NAME = "radiusmart"  # 🔹 Fill this


@router.get("/pending-orders")
def get_pending_orders(db: Session = Depends(get_db)):

    orders = db.query(Order).filter(Order.status == "pending").all()

    if not orders:
        return {"message": "No pending orders", "orders": []}

    return {
        "total_pending": len(orders),
        "orders": [
            {
                "order_id": order.id,
                "customer_name": order.customer_name,
                "customer_phone": order.customer_phone,
                "total_amount": order.total_amount,
                "created_at": order.created_at,
            }
            for order in orders
        ]
    }


@router.get("/generate-qr/{order_id}")
def generate_payment_qr(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == "paid":
        raise HTTPException(status_code=400, detail="Order already paid")

    upi_link = (
        f"upi://pay?pa={UPI_ID}"
        f"&pn={STORE_NAME}"
        f"&am={order.total_amount}"
        f"&cu=INR"
        f"&tn=ORDER_{order.id}"
    )

    qr = qrcode.make(upi_link)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return {
        "message": "Scan QR to pay",
        "order_id": order.id,
        "customer_name": order.customer_name,
        "total_amount": order.total_amount,
        "status": order.status,
        "upi_link": upi_link,
        "qr_code": img_base64
    }