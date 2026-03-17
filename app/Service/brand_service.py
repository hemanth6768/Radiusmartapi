from fastapi import HTTPException
from app.Repository.brand_repository import BrandRepository
from app.core.logger import logger


class BrandService:

    def __init__(self, repo: BrandRepository):
        self.repo = repo

    def create_brand(self, brand):
        existing = self.repo.get_by_name(brand.name)

        if existing:
            logger.warning(f"Duplicate brand: {brand.name}")
            raise HTTPException(
                status_code=400,
                detail="Brand already exists"
            )

        return self.repo.create(brand)

    def get_brands(self):
        return self.repo.get_all()

    def get_brand(self, brand_id: int):
        brand = self.repo.get_by_id(brand_id)

        if not brand:
            logger.warning(f"Brand not found id={brand_id}")
            raise HTTPException(status_code=404, detail="Brand not found")

        return brand

    def update_brand(self, brand_id: int, updates):
        brand = self.repo.get_by_id(brand_id)

        if not brand:
            logger.warning(f"Update failed, brand not found id={brand_id}")
            raise HTTPException(status_code=404, detail="Brand not found")

        return self.repo.update(brand, updates)

    def delete_brand(self, brand_id: int):
        brand = self.repo.get_by_id(brand_id)

        if not brand:
            logger.warning(f"Delete failed, brand not found id={brand_id}")
            raise HTTPException(status_code=404, detail="Brand not found")

        self.repo.delete(brand)

        return {"message": "Brand deleted successfully"}