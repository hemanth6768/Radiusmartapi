from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.Repository.product_repository import ProductRepository
from app.schemas.product import ProductCreate
from app.models.category import Category
from app.models.brand import Brand
from app.schemas.product import ProductUpdate
from app.schemas.product import VariantUpdate

class ProductService:

    @staticmethod
    def create_product(db: Session, product: ProductCreate):

        category = db.query(Category).filter(
            Category.id == product.category_id
        ).first()

        if not category:
            raise HTTPException(status_code=400, detail="Invalid category")

        if product.brand_id:
            brand = db.query(Brand).filter(
                Brand.id == product.brand_id
            ).first()

            if not brand:
                raise HTTPException(status_code=400, detail="Invalid brand")

        if len(product.variants) == 0:
            raise HTTPException(status_code=400, detail="At least one variant required")

        return ProductRepository.create_product_with_variants(db, product)

    
    @staticmethod
    def get_products(db: Session):
        return ProductRepository.get_all_products(db)


    @staticmethod
    def get_product(db: Session, product_id: int):

        product = ProductRepository.get_product_by_id(db, product_id)

        if not product:
            raise HTTPException(404, "Product not found")

        return product


    @staticmethod
    def update_product(db: Session, product_id: int, updates: ProductUpdate):

        product = ProductRepository.get_product_by_id(db, product_id)

        if not product:
            raise HTTPException(404, "Product not found")

        return ProductRepository.update_product(db, product, updates)


    @staticmethod
    def delete_product(db: Session, product_id: int):

        product = ProductRepository.get_product_by_id(db, product_id)

        if not product:
            raise HTTPException(404, "Product not found")

        ProductRepository.delete_product(db, product)

        return {"message": "Product deleted successfully"}


    @staticmethod
    def update_variant(db: Session, variant_id: int, updates: VariantUpdate):

        variant = ProductRepository.get_variant_by_id(db, variant_id)

        if not variant:
            raise HTTPException(404, "Variant not found")

        return ProductRepository.update_variant(db, variant, updates)


    @staticmethod
    def delete_variant(db: Session, variant_id: int):

        variant = ProductRepository.get_variant_by_id(db, variant_id)

        if not variant:
            raise HTTPException(404, "Variant not found")

        ProductRepository.delete_variant(db, variant)

        return {"message": "Variant deleted"}