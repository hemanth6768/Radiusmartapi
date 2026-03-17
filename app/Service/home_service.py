from app.Repository.home_repository import HomeRepository
from app.core.logger import logger


class HomeService:

    def __init__(self, repo: HomeRepository):
        self.repo = repo

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

        # Get all products in ONE query
        all_products = self.repo.get_products_by_category_ids(category_ids)

        # Group products by category_id
        product_map = {}
        for product in all_products:
            product_map.setdefault(product.category_id, []).append(product)

        sections_data = []

        for section in sections:
            categories_data = []

            for category in section.categories:

                products = product_map.get(category.id, [])[:5]

                # Prepare images
                for product in products:
                    if product.image_url:
                        product.image_url = f"/static/{product.image_url}"

                    for variant in product.variants:
                        if variant.image_url:
                            variant.image_url = f"/static/{variant.image_url}"

                next_cursor = str(products[-1].id) if products else None

                categories_data.append({
                    "id": category.id,
                    "name": category.name,
                    "products": products,
                    "next_cursor": next_cursor
                })

            sections_data.append({
                "id": section.id,
                "name": section.name,
                "categories": categories_data
            })

        return {"sections": sections_data}