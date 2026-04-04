from app.Repository.home_repository import HomeRepository
from app.Service.offer_service import OfferService
from app.core.logger import logger


class HomeService:

    def __init__(self, repo: HomeRepository, offer_service: OfferService):
        self.repo = repo
        self.offer_service = offer_service

    def get_home_data(self):

        sections = self.repo.get_sections_with_categories()

        if not sections:
            logger.warning("No sections found")
            return {"sections": []}

        # Collect all category IDs
        category_ids = []
        for section in sections:
            for category in section.categories:
                category_ids.append(category.id)

        # Get first 5 products per category — ONE DB query
        all_products = self.repo.get_products_by_category_ids(category_ids)

        # Group products by category_id
        product_map = {}
        for product in all_products:
            product_map.setdefault(product.category_id, []).append(product)

        sections_data = []

        for section in sections:
            categories_data = []

            for category in section.categories:

                # ✅ No [:5] slice here — DB already limits to 5
                products = product_map.get(category.id, [])

                # Enrich images + compute sales_price
                for product in products:
                    if product.image_url and not product.image_url.startswith("/static/"):
                        product.image_url = f"/static/{product.image_url}"

                    for variant in product.variants:
                        if variant.image_url and not variant.image_url.startswith("/static/"):
                            variant.image_url = f"/static/{variant.image_url}"

                        # Pick best active offer and compute sales_price
                        active_offers = self.offer_service.get_active_offers_for_variant(variant.id)

                        if active_offers:
                            best_offer = min(active_offers, key=lambda o: o.priority)
                            variant.sales_price = OfferService._apply_discount(
                                variant.base_price, best_offer
                            )
                        # else: keep existing sales_price as-is

                # next_cursor = last product id in this category
                # frontend uses this to call GET /home/category/{id}/products?cursor=xxx
                next_cursor = str(products[-1].id) if products else None

                categories_data.append({
                    "id": category.id,
                    "name": category.name,
                    "next_cursor": next_cursor,
                    "products": products
                })

            sections_data.append({
                "id": section.id,
                "name": section.name,
                "categories": categories_data
            })

        return {"sections": sections_data}