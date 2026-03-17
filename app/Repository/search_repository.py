from sqlalchemy.orm import Session, joinedload
from app.models.product import Product
from app.core.logger import logger


class SearchRepository:

    def __init__(self, db: Session):
        self.db = db

    def search_products(self, query: str, limit: int):
        try:
            return (
                self.db.query(Product)
                .options(
                    joinedload(Product.variants),
                    joinedload(Product.brand),
                    joinedload(Product.category)
                )
                .filter(Product.is_active == True)
                .filter(Product.name.ilike(f"%{query}%"))
                .order_by(Product.id)
                .limit(limit)
                .all()
            )

        except Exception as e:
            logger.error(f"DB Error in search: {str(e)}")
            raise