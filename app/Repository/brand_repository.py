from sqlalchemy.orm import Session
from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandUpdate
from app.core.logger import logger


class BrandRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, brand: BrandCreate):
        try:
            db_brand = Brand(**brand.model_dump())

            self.db.add(db_brand)
            self.db.commit()
            self.db.refresh(db_brand)

            logger.info(f"Brand created id={db_brand.id}")
            return db_brand

        except Exception as e:
            logger.error(f"Error creating brand: {str(e)}")
            self.db.rollback()
            raise

    def get_all(self):
     return self.db.query(Brand).all()

    def get_by_id(self, brand_id: int):
        return (
            self.db.query(Brand)
            .filter(Brand.id == brand_id)
            .first()
        )

    def get_by_name(self, name: str):
        return (
            self.db.query(Brand)
            .filter(Brand.name == name)
            .first()
        )

    def update(self, db_brand: Brand, updates: BrandUpdate):
        try:
            update_data = updates.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(db_brand, key, value)

            self.db.commit()
            self.db.refresh(db_brand)

            logger.info(f"Brand updated id={db_brand.id}")
            return db_brand

        except Exception as e:
            logger.error(f"Error updating brand: {str(e)}")
            self.db.rollback()
            raise

    def delete(self, db_brand: Brand):
        try:
            # ✅ Soft delete (recommended)
            db_brand.is_active = False
            self.db.commit()

            logger.info(f"Brand deleted id={db_brand.id}")
            return db_brand

        except Exception as e:
            logger.error(f"Error deleting brand: {str(e)}")
            self.db.rollback()
            raise