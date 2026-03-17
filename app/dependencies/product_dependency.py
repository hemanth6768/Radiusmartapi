from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Repository.product_repository import ProductRepository
from app.Service.product_service import ProductService


def get_product_repository(
    db: Session = Depends(get_db)
) -> ProductRepository:
    return ProductRepository(db)


def get_product_service(
    repo: ProductRepository = Depends(get_product_repository)
) -> ProductService:
    return ProductService(repo)