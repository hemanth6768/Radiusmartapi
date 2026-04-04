from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, select
from app.models.section import Section
from app.models.category import Category
from app.models.product import Product
from app.models.productvariant import ProductVariant
from app.models.offervariant import OfferVariant
from app.core.logger import logger

PRODUCT_PAGE_SIZE = 5


class HomeRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_sections_with_categories(self):
        """
        Load all active sections with their active categories.
        Categories are small in count so no pagination needed here.
        """
        return (
            self.db.query(Section)
            .options(joinedload(Section.categories))
            .filter(Section.is_active == True)
            .order_by(Section.display_order)
            .all()
        )

    def get_products_by_category_ids(self, category_ids: list):
        """
        Fetch first 5 products per category in ONE query using ROW_NUMBER().
        No matter how many categories — always a single DB round trip.
        """
        if not category_ids:
            return []

        # Step 1: Rank products within each category by id
        row_number = (
            func.row_number()
            .over(
                partition_by=Product.category_id,
                order_by=Product.id
            )
            .label("rn")
        )

        # Step 2: Subquery — get id + rank for active products
        subq = (
            select(Product.id, row_number)
            .where(Product.category_id.in_(category_ids))
            .where(Product.is_active == True)
            .subquery()
        )

        # Step 3: Main query — join and filter to top 5 per category
        return (
            self.db.query(Product)
            .options(
                joinedload(Product.variants)
                    .joinedload(ProductVariant.offer_variants)
                    .joinedload(OfferVariant.offer)
            )
            .join(subq, subq.c.id == Product.id)
            .where(subq.c.rn <= PRODUCT_PAGE_SIZE)
            .order_by(Product.category_id, Product.id)
            .all()
        )