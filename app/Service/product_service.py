from fastapi import HTTPException
from app.Repository.product_repository import ProductRepository
from app.core.logger import logger
from app.schemas.pagination import CursorPage
from app.utils.pagination import encode_cursor, decode_cursor
from app.models.category import Category
from app.models.brand import Brand


class ProductService:

    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create_product(self, product):
        if len(product.variants) == 0:
            raise HTTPException(400, "At least one variant required")

        return self.repo.create_product_with_variants(product)

    def get_products(self, cursor, limit):
        last_id = decode_cursor(cursor)["id"] if cursor else None

        products = self.repo.get_products_cursor(last_id, limit)

        has_more = len(products) > limit
        items = products[:limit]

        next_cursor = encode_cursor({"id": items[-1].id}) if has_more else None

        self._prepare_images(items)

        return CursorPage(items=items, next_cursor=next_cursor, has_more=has_more)

    def get_product(self, product_id: int):
        product = self.repo.get_product_by_id(product_id)

        if not product:
            logger.warning(f"Product not found id={product_id}")
            raise HTTPException(404, "Product not found")

        self._prepare_images([product])
        return product

    def get_products_by_category(self, category_id, cursor, limit):
        last_id = decode_cursor(cursor)["id"] if cursor else None

        products = self.repo.get_products_by_category_cursor(category_id, last_id, limit)

        has_more = len(products) > limit
        items = products[:limit]

        next_cursor = encode_cursor({"id": items[-1].id}) if has_more else None

        self._prepare_images(items)

        return CursorPage(items=items, next_cursor=next_cursor, has_more=has_more)

    def get_products_by_brand(self, brand_id, cursor, limit):
        last_id = decode_cursor(cursor)["id"] if cursor else None

        products = self.repo.get_products_by_brand_cursor(brand_id, last_id, limit)

        has_more = len(products) > limit
        items = products[:limit]

        next_cursor = encode_cursor({"id": items[-1].id}) if has_more else None

        self._prepare_images(items)

        return CursorPage(items=items, next_cursor=next_cursor, has_more=has_more)

    def update_product(self, product_id, updates):
        product = self.repo.get_product_by_id(product_id)

        if not product:
            raise HTTPException(404, "Product not found")

        return self.repo.update_product(product, updates)

    def delete_product(self, product_id):
        product = self.repo.get_product_by_id(product_id)

        if not product:
            raise HTTPException(404, "Product not found")

        self.repo.delete_product(product)
        return {"message": "Product deleted successfully"}

    def _prepare_images(self, products):
        for product in products:
            if product.image_url:
                product.image_url = f"/static/{product.image_url}"

            for variant in product.variants:
                if variant.image_url:
                    variant.image_url = f"/static/{variant.image_url}"