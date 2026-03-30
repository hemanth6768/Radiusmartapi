from sqlalchemy.orm import Session, joinedload
from app.models.product import Product
from app.models.productvariant import ProductVariant
from app.models.offervariant import OfferVariant
from app.core.logger import logger


class ProductRepository:

    def __init__(self, db: Session):
        self.db = db

    # Create product with variants
    def create_product_with_variants(self, product_data):
        try:
            product = Product(
                name=product_data.name,
                description=product_data.description,
                category_id=product_data.category_id,
                brand_id=product_data.brand_id,
                image_url=product_data.image_url
            )

            self.db.add(product)
            self.db.flush()

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
                self.db.add(db_variant)

            self.db.commit()
            self.db.refresh(product)

            logger.info(f"Product created id={product.id}")
            return product

        except Exception as e:
            logger.error(f"Error creating product: {str(e)}")
            self.db.rollback()
            raise

    # Base query with joins (used for all fetch APIs)
    def base_query(self):
        return (
            self.db.query(Product)
            .options(
                joinedload(Product.brand),
                joinedload(Product.category),
                joinedload(Product.variants)
                    .joinedload(ProductVariant.offer_variants)
                    .joinedload(OfferVariant.offer)   # ← chain through join table
            )
            .filter(Product.is_active == True)
            .order_by(Product.id)
        )

    # Cursor pagination
    def get_products_cursor(self, last_id: int | None, limit: int):
        query = self.base_query()

        if last_id:
            query = query.filter(Product.id > last_id)

        return query.limit(limit + 1).all()

    def get_products_by_category_cursor(self, category_id, last_id, limit):
        query = self.base_query().filter(Product.category_id == category_id)

        if last_id:
            query = query.filter(Product.id > last_id)

        return query.limit(limit + 1).all()

    def get_products_by_brand_cursor(self, brand_id, last_id, limit):
        query = self.base_query().filter(Product.brand_id == brand_id)

        if last_id:
            query = query.filter(Product.id > last_id)

        return query.limit(limit + 1).all()

    def get_product_by_id(self, product_id: int):
        return (
            self.base_query()
            .filter(Product.id == product_id)
            .first()
        )

    def update_product(self, product, updates):
        try:
            update_data = updates.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(product, key, value)

            self.db.commit()
            self.db.refresh(product)

            logger.info(f"Product updated id={product.id}")
            return product

        except Exception as e:
            logger.error(f"Error updating product: {str(e)}")
            self.db.rollback()
            raise

    def delete_product(self, product):
        try:
            # Soft delete
            product.is_active = False
            self.db.commit()

            logger.info(f"Product deleted id={product.id}")

        except Exception as e:
            logger.error(f"Error deleting product: {str(e)}")
            self.db.rollback()
            raise

    def get_variant_by_id(self, variant_id: int):
        return self.db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()

    def update_variant(self, variant, updates):
        try:
            update_data = updates.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(variant, key, value)

            self.db.commit()
            self.db.refresh(variant)

            return variant

        except Exception as e:
            logger.error(f"Error updating variant: {str(e)}")
            self.db.rollback()
            raise

    def delete_variant(self, variant):
        try:
            self.db.delete(variant)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting variant: {str(e)}")
            self.db.rollback()
            raise