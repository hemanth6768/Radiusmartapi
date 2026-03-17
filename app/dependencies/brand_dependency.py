from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Repository.brand_repository import BrandRepository
from app.Service.brand_service import BrandService


def get_brand_repository(
    db: Session = Depends(get_db)
) -> BrandRepository:
    return BrandRepository(db)


def get_brand_service(
    repo: BrandRepository = Depends(get_brand_repository)
) -> BrandService:
    return BrandService(repo)