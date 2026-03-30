from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Repository.offer_repository import OfferRepository
from app.Service.offer_service import OfferService


def get_offer_repository(
    db: Session = Depends(get_db)
) -> OfferRepository:
    return OfferRepository(db)


def get_offer_service(
    repo: OfferRepository = Depends(get_offer_repository)
) -> OfferService:
    return OfferService(repo)