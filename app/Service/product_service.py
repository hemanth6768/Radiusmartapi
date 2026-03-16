from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.Repository.product_repository import ProductRepository
from app.schemas.pagination import CursorPage
from app.schemas.product import ProductCreate, ProductUpdate, VariantUpdate
from app.utils.pagination import encode_cursor, decode_cursor
from typing import List
from app.models.category import Category
from app.models.brand import Brand


class ProductService:


    # Create product
    @staticmethod
    def create_product(db: Session, product: ProductCreate):

        category = db.query(Category).filter(
            Category.id == product.category_id
        ).first()

        if not category:
            raise HTTPException(400, "Invalid category")

        if product.brand_id:

            brand = db.query(Brand).filter(
                Brand.id == product.brand_id
            ).first()

            if not brand:
                raise HTTPException(400, "Invalid brand")

        if len(product.variants) == 0:
            raise HTTPException(400, "At least one variant required")

        return ProductRepository.create_product_with_variants(db, product)

    @staticmethod
    def create_products_bulk(db: Session, products: List[ProductCreate]):

        created_products = []

        for product in products:

            category = db.query(Category).filter(
                Category.id == product.category_id
            ).first()

            if not category:
                raise HTTPException(400, f"Invalid category {product.category_id}")

            if product.brand_id:
                brand = db.query(Brand).filter(
                    Brand.id == product.brand_id
                ).first()

                if not brand:
                    raise HTTPException(400, f"Invalid brand {product.brand_id}")

            if len(product.variants) == 0:
                raise HTTPException(400, "At least one variant required")

            created_product = ProductRepository.create_bulk_product_with_variants(
                db, product
            )

            created_products.append(created_product)

        return created_products
    # Cursor pagination for products
    @staticmethod
    def get_products(db: Session, cursor: str | None, limit: int):

        last_id = None

        if cursor:
            decoded = decode_cursor(cursor)
            last_id = decoded["id"]

        products = ProductRepository.get_products_cursor(db, last_id, limit)

        has_more = len(products) > limit
        items = products[:limit]

        next_cursor = None

        if has_more:
            next_cursor = encode_cursor({"id": items[-1].id})

        ProductService._prepare_images(items)

        return CursorPage(
            items=items,
            next_cursor=next_cursor,
            has_more=has_more
        )


    # Products by category
    @staticmethod
    def get_products_by_category(db, category_id, cursor, limit):

        last_id = None

        if cursor:
            decoded = decode_cursor(cursor)
            last_id = decoded["id"]

        products = ProductRepository.get_products_by_category_cursor(
            db, category_id, last_id, limit
        )

        has_more = len(products) > limit
        items = products[:limit]

        next_cursor = None

        if has_more:
            next_cursor = encode_cursor({"id": items[-1].id})

        ProductService._prepare_images(items)

        return CursorPage(
            items=items,
            next_cursor=next_cursor,
            has_more=has_more
        )


    # Products by brand
    @staticmethod
    def get_products_by_brand(db, brand_id, cursor, limit):

        last_id = None

        if cursor:
            decoded = decode_cursor(cursor)
            last_id = decoded["id"]

        products = ProductRepository.get_products_by_brand_cursor(
            db, brand_id, last_id, limit
        )

        has_more = len(products) > limit
        items = products[:limit]

        next_cursor = None

        if has_more:
            next_cursor = encode_cursor({"id": items[-1].id})

        ProductService._prepare_images(items)

        return CursorPage(
            items=items,
            next_cursor=next_cursor,
            has_more=has_more
        )


    # Single product
    @staticmethod
    def get_product(db: Session, product_id: int):

        product = ProductRepository.get_product_by_id(db, product_id)

        if not product:
            raise HTTPException(404, "Product not found")

        ProductService._prepare_images([product])

        return product


    # Update product
    @staticmethod
    def update_product(db: Session, product_id: int, updates: ProductUpdate):

        product = ProductRepository.get_product_by_id(db, product_id)

        if not product:
            raise HTTPException(404, "Product not found")

        return ProductRepository.update_product(db, product, updates)


    # Delete product
    @staticmethod
    def delete_product(db: Session, product_id: int):

        product = ProductRepository.get_product_by_id(db, product_id)

        if not product:
            raise HTTPException(404, "Product not found")

        ProductRepository.delete_product(db, product)

        return {"message": "Product deleted successfully"}


    # Update variant
    @staticmethod
    def update_variant(db: Session, variant_id: int, updates: VariantUpdate):

        variant = ProductRepository.get_variant_by_id(db, variant_id)

        if not variant:
            raise HTTPException(404, "Variant not found")

        return ProductRepository.update_variant(db, variant, updates)


    # Delete variant
    @staticmethod
    def delete_variant(db: Session, variant_id: int):

        variant = ProductRepository.get_variant_by_id(db, variant_id)

        if not variant:
            raise HTTPException(404, "Variant not found")

        ProductRepository.delete_variant(db, variant)

        return {"message": "Variant deleted successfully"}


    # Helper to prepare static image URLs
    @staticmethod
    def _prepare_images(products):

        for product in products:

            if product.image_url:
                product.image_url = f"/static/{product.image_url}"

            for variant in product.variants:
                if variant.image_url:
                    variant.image_url = f"/static/{variant.image_url}"