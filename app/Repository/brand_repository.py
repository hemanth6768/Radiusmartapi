from sqlalchemy.orm import Session
from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandUpdate


class BrandRepository:

    @staticmethod
    def create(db: Session, brand: BrandCreate):
        db_brand = Brand(**brand.model_dump())

        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)

        return db_brand


    @staticmethod
    def get_all(db: Session):
        return db.query(Brand).all()


    @staticmethod
    def get_by_id(db: Session, brand_id: int):
        return db.query(Brand).filter(Brand.id == brand_id).first()


    @staticmethod
    def update(db: Session, db_brand: Brand, updates: BrandUpdate):

        update_data = updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_brand, key, value)

        db.commit()
        db.refresh(db_brand)

        return db_brand


    @staticmethod
    def delete(db: Session, db_brand: Brand):
        db.delete(db_brand)
        db.commit()