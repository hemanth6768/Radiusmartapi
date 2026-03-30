from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Repository.product_repository import ProductRepository
from app.Repository.offer_repository import OfferRepository
from app.Service.product_service import ProductService
from app.Service.offer_service import OfferService


def get_product_repository(
    db: Session = Depends(get_db)
) -> ProductRepository:
    return ProductRepository(db)


def get_offer_repository(
    db: Session = Depends(get_db)
) -> OfferRepository:
    return OfferRepository(db)


def get_product_service(
    repo: ProductRepository = Depends(get_product_repository),
    offer_repo: OfferRepository = Depends(get_offer_repository),
) -> ProductService:
    offer_service = OfferService(repo=offer_repo)
    return ProductService(repo=repo, offer_service=offer_service)