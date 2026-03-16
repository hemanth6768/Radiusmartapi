from sqlalchemy.orm import Session, joinedload
from app.models.product import Product
from app.models.productvariant import ProductVariant


class ProductRepository:

    # Create product with variants
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
        db.flush()

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
    def create_bulk_product_with_variants(db, product_data):

        product = Product(
            name=product_data.name,
            description=product_data.description,
            category_id=product_data.category_id,
            brand_id=product_data.brand_id,
            image_url=product_data.image_url,
            is_active=product_data.is_active
        )

        db.add(product)
        db.flush()

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
    
    # Base query used by all pagination queries
    @staticmethod
    def base_product_query(db: Session):

        return (
            db.query(Product)
            .options(
                joinedload(Product.brand),
                joinedload(Product.category),
                joinedload(Product.variants)
            )
            .order_by(Product.id)
        )


    # Cursor paginated product list
    @staticmethod
    def get_products_cursor(db: Session, last_id: int | None, limit: int):

        query = ProductRepository.base_product_query(db)

        if last_id:
            query = query.filter(Product.id > last_id)

        return query.limit(limit + 1).all()


    # Cursor paginated products by category
    @staticmethod
    def get_products_by_category_cursor(db: Session, category_id, last_id, limit):

        query = ProductRepository.base_product_query(db).filter(
            Product.category_id == category_id
        )

        if last_id:
            query = query.filter(Product.id > last_id)

        return query.limit(limit + 1).all()


    # Cursor paginated products by brand
    @staticmethod
    def get_products_by_brand_cursor(db: Session, brand_id, last_id, limit):

        query = ProductRepository.base_product_query(db).filter(
            Product.brand_id == brand_id
        )

        if last_id:
            query = query.filter(Product.id > last_id)

        return query.limit(limit + 1).all()


    # Get single product
    @staticmethod
    def get_product_by_id(db: Session, product_id: int):

        return (
            db.query(Product)
            .options(
                joinedload(Product.brand),
                joinedload(Product.category),
                joinedload(Product.variants)
            )
            .filter(Product.id == product_id)
            .first()
        )


    # Update product
    @staticmethod
    def update_product(db: Session, product: Product, updates):

        update_data = updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)

        return product


    # Delete product
    @staticmethod
    def delete_product(db: Session, product: Product):

        db.delete(product)
        db.commit()


    # Get variant
    @staticmethod
    def get_variant_by_id(db: Session, variant_id: int):

        return db.query(ProductVariant).filter(
            ProductVariant.id == variant_id
        ).first()


    # Update variant
    @staticmethod
    def update_variant(db: Session, variant, updates):

        update_data = updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(variant, key, value)

        db.commit()
        db.refresh(variant)

        return variant


    # Delete variant
    @staticmethod
    def delete_variant(db: Session, variant):

        db.delete(variant)
        db.commit()