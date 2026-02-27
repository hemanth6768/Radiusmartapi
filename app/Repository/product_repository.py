from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:

    @staticmethod
    def create(db: Session, product: ProductCreate):
        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def get_all(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def update(db: Session, db_product: Product, updates: ProductUpdate):
        update_data = updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def delete(db: Session, db_product: Product):
        db.delete(db_product)
        db.commit()

    @staticmethod
    def get_by_category(db: Session, category_id: int):
        return db.query(Product).filter(Product.category_id == category_id).all()