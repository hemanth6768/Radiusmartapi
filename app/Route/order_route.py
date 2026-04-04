import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies.auth_dependency import get_current_user, require_role
from app.dependencies.order_dependency import get_order_service
from app.exceptions.order_exception import (
    AddressAccessDeniedException,
    AddressNotFoundException,
    InsufficientStockException,
    InvalidOrderRequestException,
    OrderNotFoundException,
    UserNotFoundException,
)
from app.schemas.order import (
    CheckoutPrefillResponse,
    OrderDetailResponse,
    OrderListResponse,
    OrderStatus,
    PlaceOrderRequest,
    PlaceOrderResponse,
    VerifyPaymentRequest,
    VerifyPaymentResponse,
)
from app.schemas.pagination import CursorPage
from app.Service.order_service import OrderService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/orders", tags=["Orders"])


# ─── Exception → HTTP mapping ─────────────────────────────────────────────────

def _handle_domain_exception(exc: Exception) -> HTTPException:
    mapping = {
        UserNotFoundException:        status.HTTP_404_NOT_FOUND,
        AddressNotFoundException:     status.HTTP_404_NOT_FOUND,
        OrderNotFoundException:       status.HTTP_404_NOT_FOUND,
        AddressAccessDeniedException: status.HTTP_403_FORBIDDEN,
        InsufficientStockException:   status.HTTP_409_CONFLICT,
        InvalidOrderRequestException: status.HTTP_422_UNPROCESSABLE_ENTITY,
    }
    code = mapping.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
    return HTTPException(status_code=code, detail=str(exc))


# ─── Checkout prefill ─────────────────────────────────────────────────────────

@router.get(
    "/checkout/prefill",
    response_model=CheckoutPrefillResponse,
    summary="Get checkout prefill data",
)
def get_checkout_prefill(
    current_user: dict    = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    user_id = int(current_user["sub"])
    try:
        return service.get_checkout_prefill(user_id)
    except (UserNotFoundException, AddressNotFoundException) as exc:
        raise _handle_domain_exception(exc)
    except Exception:
        logger.exception("Unexpected error in get_checkout_prefill user=%d", user_id)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# ─── Place order ──────────────────────────────────────────────────────────────

@router.post(
    "/",
    response_model=PlaceOrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Place an order",
    description="Creates DB order + Razorpay order. Returns razorpay_order_id and razorpay_key for the frontend modal.",
)
def place_order(
    payload: PlaceOrderRequest,
    current_user: dict    = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    user_id = int(current_user["sub"])
    try:
        return service.place_order(user_id, payload)
    except (
        UserNotFoundException,
        AddressNotFoundException,
        OrderNotFoundException,
        AddressAccessDeniedException,
        InvalidOrderRequestException,
        InsufficientStockException,
    ) as exc:
        raise _handle_domain_exception(exc)
    except Exception:
        logger.exception("Unexpected error in place_order user=%d", user_id)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# ─── Verify payment ───────────────────────────────────────────────────────────

@router.post(
    "/verify-payment",
    response_model=VerifyPaymentResponse,
    summary="Verify Razorpay payment",
    description="Verifies HMAC signature from Razorpay. On success sets order status=confirmed and payment_status=paid.",
)
def verify_payment(
    payload: VerifyPaymentRequest,
    current_user: dict    = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    user_id = int(current_user["sub"])
    try:
        return service.verify_payment(user_id, payload)
    except (OrderNotFoundException, InvalidOrderRequestException) as exc:
        raise _handle_domain_exception(exc)
    except Exception:
        logger.exception("Unexpected error in verify_payment user=%d", user_id)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# ─── My orders ────────────────────────────────────────────────────────────────

@router.get(
    "/my",
    response_model=CursorPage[OrderListResponse],
    summary="Get my orders",
)
def get_my_orders(
    cursor: Optional[str] = Query(None),
    limit:  int           = Query(10, ge=1, le=50),
    current_user: dict    = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    user_id = int(current_user["sub"])
    try:
        page       = service.get_my_orders(user_id, cursor, limit)
        page.items = [OrderListResponse.from_order(o) for o in page.items]
        return page
    except Exception:
        logger.exception("Unexpected error in get_my_orders user=%d", user_id)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get(
    "/my/{order_id}",
    response_model=OrderDetailResponse,
    summary="Get my order by ID",
)
def get_my_order_by_id(
    order_id: int,
    current_user: dict    = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    user_id = int(current_user["sub"])
    try:
        order = service.get_my_order_by_id(order_id, user_id)
        return OrderDetailResponse.from_order(order)
    except OrderNotFoundException as exc:
        raise _handle_domain_exception(exc)
    except Exception:
        logger.exception("Unexpected error in get_my_order_by_id user=%d order=%d", user_id, order_id)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# ─── Admin — all orders ───────────────────────────────────────────────────────

@router.get(
    "/admin",
    response_model=CursorPage[OrderListResponse],
    summary="[Admin] Get all orders",
)
def get_all_orders(
    cursor:    Optional[str]         = Query(None),
    limit:     int                   = Query(10, ge=1, le=100),
    status:    Optional[OrderStatus] = Query(None),
    from_date: Optional[datetime]    = Query(None),
    to_date:   Optional[datetime]    = Query(None),
    current_user: dict               = Depends(require_role("Admin")),
    service: OrderService            = Depends(get_order_service),
):
    try:
        page       = service.get_all_orders(
            cursor=cursor,
            limit=limit,
            status=status.value if status else None,
            from_date=from_date,
            to_date=to_date,
        )
        page.items = [OrderListResponse.from_order(o) for o in page.items]
        return page
    except Exception:
        logger.exception("Unexpected error in get_all_orders (admin)")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get(
    "/admin/{order_id}",
    response_model=OrderDetailResponse,
    summary="[Admin] Get any order by ID",
)
def get_order_by_id_admin(
    order_id: int,
    current_user: dict    = Depends(require_role("admin")),
    service: OrderService = Depends(get_order_service),
):
    try:
        order = service.get_order_by_id_admin(order_id)
        return OrderDetailResponse.from_order(order)
    except OrderNotFoundException as exc:
        raise _handle_domain_exception(exc)
    except Exception:
        logger.exception("Unexpected error in get_order_by_id_admin order=%d", order_id)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")