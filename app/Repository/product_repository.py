from sqlalchemy.orm import Session,joinedload
from app.models.product import Product
from app.models.productvariant import ProductVariant
from fastapi import HTTPException

class ProductRepository:

    @staticmethod
    def create_product_with_variants(db: Session, product_data):

        product = Product(
            name=product_data.name,
            description=product_data.description,
            category_id=product_data.category_id,
            brand_id=product_data.brand_id,
            image_url=product_data.image_url
        )

        db.add(product)
        db.flush()   # generate product.id before commit

        for variant in product_data.variants:

            db_variant = ProductVariant(
                product_id=product.id,
                pricing_model=variant.pricing_model,
                base_unit=variant.base_unit,
                value=variant.value,
                base_price=variant.base_price,
                stock_quantity=variant.stock_quantity,
                image_url=variant.image_url
            )

            db.add(db_variant)

        db.commit()
        db.refresh(product)

        return product
    

    @staticmethod
    def get_all_products(db: Session):
        try:
            products = (
                db.query(Product)
                .options(
                    joinedload(Product.brand),
                    joinedload(Product.category),
                    joinedload(Product.variants)
                )
                .all()
            )

            if not products:
                raise HTTPException(
                    status_code=404,
                    detail="No products found"
                )

            return products

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch products: {str(e)}"
            )
        

    @staticmethod
    def get_product_by_id(db: Session, product_id: int):

        product = (
            db.query(Product)
            .options(
                joinedload(Product.brand),
                joinedload(Product.category),
                joinedload(Product.variants)
            )
            .filter(Product.id == product_id)
            .first()
        )

        return product
    

    @staticmethod
    def get_products_by_category(db, category_id: int):
        try:
            products = (
                db.query(Product)
                .filter(Product.category_id == category_id)
                .options(
                    joinedload(Product.brand),
                    joinedload(Product.category),
                    joinedload(Product.variants)
                )
                .all()
            )

            if not products:
                raise HTTPException(
                    status_code=404,
                    detail="No products found for this category"
                )

            return products

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch products"
            )

    @staticmethod
    def update_product(db: Session, product: Product, updates):

        update_data = updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)

        return product


    @staticmethod
    def delete_product(db: Session, product: Product):
        db.delete(product)
        db.commit()


    @staticmethod
    def get_variant_by_id(db: Session, variant_id: int):
        return db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()


    @staticmethod
    def update_variant(db: Session, variant, updates):

        update_data = updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(variant, key, value)

        db.commit()
        db.refresh(variant)

        return variant


    @staticmethod
    def delete_variant(db: Session, variant):
        db.delete(variant)
        db.commit()