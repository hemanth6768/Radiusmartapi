from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.product import Product
from app.models.category import Category
from app.Repository.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    @staticmethod
    def create_product(db: Session, product: ProductCreate):

        # Validate category exists
        category = db.query(Category).filter(Category.id == product.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Invalid category")

        if product.price < 0:
            raise HTTPException(status_code=400, detail="Price cannot be negative")

        return ProductRepository.create(db, product)

    @staticmethod
    def get_products(db: Session):
        return ProductRepository.get_all(db)

    @staticmethod
    def get_product(db: Session, product_id: int):
        product = ProductRepository.get_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    def update_product(db: Session, product_id: int, updates: ProductUpdate):

        product = ProductRepository.get_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if updates.price is not None and updates.price < 0:
            raise HTTPException(status_code=400, detail="Price cannot be negative")

        return ProductRepository.update(db, product, updates)

    @staticmethod
    def delete_product(db: Session, product_id: int):
        product = ProductRepository.get_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        ProductRepository.delete(db, product)
        return {"message": "Product deleted successfully"}

    
    @staticmethod
    def get_products_by_category(db: Session, category_id: int):

    # Validate category exists
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
           raise HTTPException(status_code=404, detail="Category not found")

        return ProductRepository.get_by_category(db, category_id)