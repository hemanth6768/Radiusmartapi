from fastapi import HTTPException
from app.Repository.product_repository import ProductRepository
from app.Service.offer_service import OfferService
from app.core.logger import logger
from app.schemas.pagination import CursorPage
from app.schemas.product import VariantUpdate
from app.utils.pagination import encode_cursor, decode_cursor
from app.models.productvariant import ProductVariant


class ProductService:

    def __init__(self, repo: ProductRepository, offer_service: OfferService):
        self.repo = repo
        self.offer_service = offer_service

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

        self._prepare_variants(items)
        return CursorPage(items=items, next_cursor=next_cursor, has_more=has_more)

    def get_product(self, product_id: int):
        product = self.repo.get_product_by_id(product_id)
        if not product:
            logger.warning(f"Product not found id={product_id}")
            raise HTTPException(404, "Product not found")

        self._prepare_variants([product])
        return product

    def get_products_by_category(self, category_id, cursor, limit):
        last_id = decode_cursor(cursor)["id"] if cursor else None
        products = self.repo.get_products_by_category_cursor(category_id, last_id, limit)

        has_more = len(products) > limit
        items = products[:limit]
        next_cursor = encode_cursor({"id": items[-1].id}) if has_more else None

        self._prepare_variants(items)
        return CursorPage(items=items, next_cursor=next_cursor, has_more=has_more)

    def get_products_by_brand(self, brand_id, cursor, limit):
        last_id = decode_cursor(cursor)["id"] if cursor else None
        products = self.repo.get_products_by_brand_cursor(brand_id, last_id, limit)

        has_more = len(products) > limit
        items = products[:limit]
        next_cursor = encode_cursor({"id": items[-1].id}) if has_more else None

        self._prepare_variants(items)
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

    # ------------------------------------------------------------------ #
    #  Variant methods                                                     #
    # ------------------------------------------------------------------ #

    def update_variant(self, variant_id: int, updates: VariantUpdate):
        variant = self.repo.get_variant_by_id(variant_id)
        if not variant:
            raise HTTPException(404, "Variant not found")
        return self.repo.update_variant(variant, updates)

    def delete_variant(self, variant_id: int):
        variant = self.repo.get_variant_by_id(variant_id)
        if not variant:
            raise HTTPException(404, "Variant not found")
        self.repo.delete_variant(variant)
        return {"message": f"Variant {variant_id} deleted successfully"}

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    def _prepare_variants(self, products):
        for product in products:
            if product.image_url:
                product.image_url = f"/static/{product.image_url}"

            for variant in product.variants:
                if variant.image_url:
                    variant.image_url = f"/static/{variant.image_url}"

                active_offers = self.offer_service.get_active_offers_for_variant(variant.id)

                if active_offers:
                    best_offer = min(active_offers, key=lambda o: o.priority)
                    variant.sales_price = OfferService._apply_discount(
                        variant.base_price, best_offer
                    )