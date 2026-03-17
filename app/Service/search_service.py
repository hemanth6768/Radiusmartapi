from fastapi import HTTPException
from app.Repository.search_repository import SearchRepository
from app.core.logger import logger


class SearchService:

    def __init__(self, repo: SearchRepository):
        self.repo = repo

    def search_products(self, query: str, limit: int):

        try:
            # Validation
            if not query.strip():
                logger.warning("Empty search query received")
                raise HTTPException(
                    status_code=400,
                    detail="Search query cannot be empty"
                )

            products = self.repo.search_products(query, limit)

            # Prepare images
            for product in products:
                if product.image_url:
                    product.image_url = f"/static/{product.image_url}"

                for variant in product.variants:
                    if variant.image_url:
                        variant.image_url = f"/static/{variant.image_url}"

            logger.info(f"Search success query='{query}' count={len(products)}")

            return products

        except HTTPException:
            # Already handled → just rethrow
            raise

        except Exception as e:
            logger.error(f"Search failed: {str(e)}")

            raise HTTPException(
                status_code=500,
                detail="Something went wrong while searching products"
            )