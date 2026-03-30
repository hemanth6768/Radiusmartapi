from sqlalchemy.orm import Session, joinedload
from app.models.section import Section
from app.models.category import Category
from app.models.product import Product
from app.models.productvariant import ProductVariant
from app.models.offervariant import OfferVariant
from app.core.logger import logger


class HomeRepository:

    def __init__(self, db: Session):
        self.db = db

    # Get sections with categories (optimized)
    def get_sections_with_categories(self):
        return (
            self.db.query(Section)
            .options(joinedload(Section.categories))
            .filter(Section.is_active == True)
            .order_by(Section.display_order)
            .all()
        )

    # Get products for multiple categories (optimized)
    def get_products_by_category_ids(self, category_ids, limit=5):
        return (
            self.db.query(Product)
            .options(
                joinedload(Product.variants)
                    .joinedload(ProductVariant.offer_variants)
                    .joinedload(OfferVariant.offer)   # ← load offer chain
            )
            .filter(Product.category_id.in_(category_ids))
            .filter(Product.is_active == True)
            .order_by(Product.id)
            .all()
        )