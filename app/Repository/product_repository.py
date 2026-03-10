from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.productvariant import ProductVariant


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
        return db.query(Product).all()


    @staticmethod
    def get_product_by_id(db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()


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