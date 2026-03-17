from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Repository.search_repository import SearchRepository
from app.Service.search_service import SearchService


def get_search_repository(
    db: Session = Depends(get_db)
) -> SearchRepository:
    return SearchRepository(db)


def get_search_service(
    repo: SearchRepository = Depends(get_search_repository)
) -> SearchService:
    return SearchService(repo)