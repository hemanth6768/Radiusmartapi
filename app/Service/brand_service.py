from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.Repository.brand_repository import BrandRepository
from app.schemas.brand import BrandCreate, BrandUpdate
from app.models.brand import Brand


class BrandService:


    @staticmethod
    def create_brand(db: Session, brand: BrandCreate):

        existing = db.query(Brand).filter(Brand.name == brand.name).first()

        if existing:
            raise HTTPException(status_code=400, detail="Brand already exists")

        return BrandRepository.create(db, brand)


    @staticmethod
    def get_brands(db: Session):
        return BrandRepository.get_all(db)


    @staticmethod
    def get_brand(db: Session, brand_id: int):

        brand = BrandRepository.get_by_id(db, brand_id)

        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

        return brand


    @staticmethod
    def update_brand(db: Session, brand_id: int, updates: BrandUpdate):

        brand = BrandRepository.get_by_id(db, brand_id)

        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

        return BrandRepository.update(db, brand, updates)


    @staticmethod
    def delete_brand(db: Session, brand_id: int):

        brand = BrandRepository.get_by_id(db, brand_id)

        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

        BrandRepository.delete(db, brand)

        return {"message": "Brand deleted successfully"}