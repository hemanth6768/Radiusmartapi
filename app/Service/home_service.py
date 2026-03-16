from app.Repository.home_repository import HomeRepository


class HomeService:

    @staticmethod
    def get_home_data(db):

        sections_data = []

        sections = HomeRepository.get_sections(db)

        for section in sections:

            categories_data = []

            categories = HomeRepository.get_categories_by_section(db, section.id)

            for category in categories:

                products = HomeRepository.get_products_by_category(
                    db,
                    category.id,
                    limit=5
                )

                for product in products:

                    if product.image_url:
                        product.image_url = f"/static/{product.image_url}"

                    for variant in product.variants:

                        if variant.image_url:
                            variant.image_url = f"/static/{variant.image_url}"

                next_cursor = None
                if products:
                    next_cursor = str(products[-1].id)

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