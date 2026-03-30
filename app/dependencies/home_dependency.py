from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Repository.home_repository import HomeRepository
from app.Repository.offer_repository import OfferRepository
from app.Service.home_service import HomeService
from app.Service.offer_service import OfferService


def get_home_repository(
    db: Session = Depends(get_db)
) -> HomeRepository:
    return HomeRepository(db)


def get_offer_repository(
    db: Session = Depends(get_db)
) -> OfferRepository:
    return OfferRepository(db)


def get_home_service(
    repo: HomeRepository = Depends(get_home_repository),
    offer_repo: OfferRepository = Depends(get_offer_repository),
) -> HomeService:
    offer_service = OfferService(repo=offer_repo)
    return HomeService(repo=repo, offer_service=offer_service)