"""
Order Dependencies
──────────────────
FastAPI dependency injection wiring.
Each layer is independently injectable and testable.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.Repository.order_repository import OrderRepository
from app.Service.order_service import OrderService


def get_order_repository(
    db: Session = Depends(get_db),
) -> OrderRepository:
    return OrderRepository(db)


def get_order_service(
    repo: OrderRepository = Depends(get_order_repository),
) -> OrderService:
    return OrderService(repo)