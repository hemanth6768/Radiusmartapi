from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Repository.home_repository import HomeRepository
from app.Service.home_service import HomeService


def get_home_repository(
    db: Session = Depends(get_db)
) -> HomeRepository:
    return HomeRepository(db)


def get_home_service(
    repo: HomeRepository = Depends(get_home_repository)
) -> HomeService:
    return HomeService(repo)