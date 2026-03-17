from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Repository.category_repository import CategoryRepository
from app.Service.category_service import CategoryService


def get_category_repository(
    db: Session = Depends(get_db)
) -> CategoryRepository:
    return CategoryRepository(db)


def get_category_service(
    repo: CategoryRepository = Depends(get_category_repository)
) -> CategoryService:
    return CategoryService(repo)