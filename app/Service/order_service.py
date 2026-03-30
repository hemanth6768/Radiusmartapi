import os
import hmac
import hashlib
import logging
import razorpay
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from dotenv import load_dotenv

from app.models.order        import Order
from app.models.orderitem    import OrderItem
from app.models.user_address import UserAddress

from app.exceptions.order_exception import InvalidOrderRequestException
from app.Repository.order_repository import OrderRepository
from app.schemas.order import (
    CheckoutPrefillResponse,
    OrderItemOut,
    PlaceOrderRequest,
    PlaceOrderResponse,
    VerifyPaymentRequest,
    VerifyPaymentResponse,
)
from app.schemas.pagination import CursorPage
from app.utils.pagination import encode_cursor, decode_cursor

load_dotenv()

logger = logging.getLogger(__name__)

# ─── Razorpay client ──────────────────────────────────────────────────────────

_rz_client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET"),
    )
)


# ─────────────────────────────────────────────
# INTERNAL VALUE OBJECTS
# ─────────────────────────────────────────────

@dataclass
class ResolvedAddress:
    customer_name:    str
    customer_phone:   str
    customer_email:   str
    customer_address: str
    city:             str
    pincode:          str
    apartment_name:   Optional[str] = None
    door_number:      Optional[str] = None
    address_id:       Optional[int] = None


@dataclass
class ComputedItem:
    variant_id:      int
    quantity:        float
    unit_price:      float
    discount_amount: float
    final_price:     float


# ─────────────────────────────────────────────
# SERVICE
# ─────────────────────────────────────────────

class OrderService:

    def __init__(self, repo: OrderRepository):
        self._repo = repo

    # ─── Checkout prefill ─────────────────────────────────────────────────────

    def get_checkout_prefill(self, user_id: int) -> CheckoutPrefillResponse:
        user    = self._repo.get_user_by_id(user_id)
        default = self._repo.get_default_address(user_id)

        if not default:
            return CheckoutPrefillResponse(
                has_default=False,
                customer_email=user.email,
                customer_name=(
                    f"{user.first_name or ''} {user.last_name or ''}".strip() or None
                ),
            )

        return CheckoutPrefillResponse(
            has_default=True,
            address_id=default.id,
            customer_name=default.customer_name,
            customer_phone=default.customer_phone,
            customer_email=user.email,
            apartment_name=default.apartment_name,
            door_number=default.door_number,
            address=default.address,
            city=default.city,
            pincode=default.pincode,
            label=default.label,
        )

    # ─── Place order ──────────────────────────────────────────────────────────

    def place_order(
        self,
        user_id: int,
        payload: PlaceOrderRequest,
    ) -> PlaceOrderResponse:
        user = self._repo.get_user_by_id(user_id)

        resolved                     = self._resolve_address(user_id, user.email, payload)
        computed_items, total_amount = self._compute_items(payload.items)

        # 1. Create order in DB — status=pending, payment_status=pending
        order = Order(
            user_id=user_id,
            address_id=resolved.address_id,
            customer_name=resolved.customer_name,
            customer_email=resolved.customer_email,
            customer_phone=resolved.customer_phone,
            apartment_name=resolved.apartment_name,
            door_number=resolved.door_number,
            customer_address=resolved.customer_address,
            city=resolved.city,
            pincode=resolved.pincode,
            total_amount=total_amount,
            status="pending",
            payment_status="pending",
        )
        order = self._repo.create_order(order)

        # 2. Create order items
        order_items = [
            OrderItem(
                order_id=order.id,
                variant_id=ci.variant_id,
                quantity=ci.quantity,
                unit_price=ci.unit_price,
                discount_amount=ci.discount_amount,
                final_price=ci.final_price,
            )
            for ci in computed_items
        ]
        self._repo.create_order_items(order_items)

        # 3. Create Razorpay order and save rz order id to DB
        rz_order = _rz_client.order.create({
            "amount":   int(total_amount * 100),  # must be in paise
            "currency": "INR",
            "receipt":  str(order.id),
        })
        order.razorpay_order_id = rz_order["id"]
        order = self._repo.save(order)

        logger.info(
            "Order %d created for user %d — total %.2f — rz_order %s",
            order.id, user_id, total_amount, rz_order["id"],
        )

        return PlaceOrderResponse(
            order_id=order.id,
            status=order.status,
            payment_status=order.payment_status,
            total_amount=order.total_amount,
            customer_name=order.customer_name,
            customer_email=order.customer_email,
            customer_phone=order.customer_phone,
            customer_address=order.customer_address,
            city=order.city,
            pincode=order.pincode,
            razorpay_order_id=rz_order["id"],
            razorpay_key=os.getenv("RAZORPAY_KEY_ID"),
            items=[
                OrderItemOut(
                    variant_id=ci.variant_id,
                    quantity=ci.quantity,
                    unit_price=ci.unit_price,
                    discount_amount=ci.discount_amount,
                    final_price=ci.final_price,
                )
                for ci in computed_items
            ],
        )

    # ─── Verify payment ───────────────────────────────────────────────────────

    def verify_payment(
        self,
        user_id: int,
        payload: VerifyPaymentRequest,
    ) -> VerifyPaymentResponse:

        # 1. Find the order by razorpay_order_id
        order = self._repo.get_order_by_razorpay_order_id(
            payload.razorpay_order_id, user_id
        )

        # 2. Verify HMAC-SHA256 signature — never skip this
        body     = f"{payload.razorpay_order_id}|{payload.razorpay_payment_id}"
        expected = hmac.new(
            key=os.getenv("RAZORPAY_KEY_SECRET").encode(),
            msg=body.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(expected, payload.razorpay_signature):
            logger.warning(
                "Signature mismatch — order %d user %d", order.id, user_id
            )
            raise InvalidOrderRequestException(
                "Payment verification failed — invalid signature"
            )

        # 3. Update order — confirmed + paid
        now                       = datetime.now(timezone.utc)
        order.status              = "confirmed"
        order.payment_status      = "paid"
        order.razorpay_payment_id = payload.razorpay_payment_id
        order.payment_method      = payload.payment_method
        order.paid_at             = now
        order = self._repo.save(order)

        logger.info(
            "Payment verified — order %d user %d payment_id %s",
            order.id, user_id, payload.razorpay_payment_id,
        )

        return VerifyPaymentResponse(
            success=True,
            order_id=order.id,
            status=order.status,
            payment_status=order.payment_status,
            paid_at=order.paid_at,
        )

    # ─── Get my orders ────────────────────────────────────────────────────────

    def get_my_orders(
        self,
        user_id: int,
        cursor:  Optional[str],
        limit:   int,
    ) -> CursorPage:
        last_id     = decode_cursor(cursor)["id"] if cursor else None
        orders      = self._repo.get_my_orders_cursor(user_id, last_id, limit)
        has_more    = len(orders) > limit
        items       = orders[:limit]
        next_cursor = encode_cursor({"id": items[-1].id}) if has_more else None
        return CursorPage(items=items, next_cursor=next_cursor, has_more=has_more)

    # ─── Get single order (current user) ─────────────────────────────────────

    def get_my_order_by_id(self, order_id: int, user_id: int) -> Order:
        return self._repo.get_order_by_id(order_id, user_id)

    # ─── Admin — all orders ───────────────────────────────────────────────────

    def get_all_orders(
        self,
        cursor:    Optional[str],
        limit:     int,
        status:    Optional[str]      = None,
        from_date: Optional[datetime] = None,
        to_date:   Optional[datetime] = None,
    ) -> CursorPage:
        last_id     = decode_cursor(cursor)["id"] if cursor else None
        orders      = self._repo.get_all_orders_cursor(last_id, limit, status, from_date, to_date)
        has_more    = len(orders) > limit
        items       = orders[:limit]
        next_cursor = encode_cursor({"id": items[-1].id}) if has_more else None
        return CursorPage(items=items, next_cursor=next_cursor, has_more=has_more)

    # ─── Admin — single order ─────────────────────────────────────────────────

    def get_order_by_id_admin(self, order_id: int) -> Order:
        return self._repo.get_order_by_id_admin(order_id)

    # ─── Private helpers ──────────────────────────────────────────────────────

    def _resolve_address(
        self,
        user_id:    int,
        user_email: str,
        payload:    PlaceOrderRequest,
    ) -> ResolvedAddress:
        if payload.use_address_id:
            saved = self._repo.get_address_by_id(payload.use_address_id, user_id)
            return ResolvedAddress(
                customer_name=saved.customer_name,
                customer_phone=saved.customer_phone,
                customer_email=user_email,
                apartment_name=saved.apartment_name,
                door_number=saved.door_number,
                customer_address=saved.address,
                city=saved.city,
                pincode=saved.pincode,
                address_id=saved.id,
            )

        missing = payload.missing_manual_fields()
        if missing:
            raise InvalidOrderRequestException(
                f"Missing required fields: {', '.join(missing)}"
            )

        self._repo.clear_default_address(user_id)

        new_addr = UserAddress(
            user_id=user_id,
            customer_name=payload.customer_name,
            customer_phone=payload.customer_phone,
            apartment_name=payload.apartment_name,
            door_number=payload.door_number,
            address=payload.customer_address,
            city=payload.city,
            pincode=payload.pincode,
            is_default=True,
        )
        new_addr = self._repo.create_address(new_addr)
        logger.info("Saved new default address %d for user %d", new_addr.id, user_id)

        return ResolvedAddress(
            customer_name=payload.customer_name,
            customer_phone=payload.customer_phone,
            customer_email=payload.customer_email,
            apartment_name=payload.apartment_name,
            door_number=payload.door_number,
            customer_address=payload.customer_address,
            city=payload.city,
            pincode=payload.pincode,
            address_id=new_addr.id,
        )

    def _compute_items(self, items) -> Tuple[List[ComputedItem], float]:
        computed: List[ComputedItem] = []
        total = 0.0

        for item in items:
            variant         = self._repo.get_variant_by_id(item.variant_id)
            self._repo.check_stock(variant, item.quantity)
            unit_price      = variant.base_price
            discount_amount = self._apply_discount(variant, item.quantity)
            final_price     = (unit_price - discount_amount) * item.quantity
            computed.append(ComputedItem(
                variant_id=item.variant_id,
                quantity=item.quantity,
                unit_price=unit_price,
                discount_amount=discount_amount,
                final_price=round(final_price, 2),
            ))
            total += final_price

        return computed, round(total, 2)

    def _apply_discount(self, variant, quantity: float) -> float:
        """
        Centralised discount hook.
        Returns per-unit discount amount.
        Replace with coupon / bulk-pricing logic as needed.
        """
        return 0.0