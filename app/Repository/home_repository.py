from sqlalchemy.orm import Session ,joinedload
from app.models.section import Section
from app.models.category import Category
from app.models.product import Product


class HomeRepository:

    @staticmethod
    def get_sections(db: Session):
        return db.query(Section).all()

    @staticmethod
    def get_categories_by_section(db: Session, section_id: int):
        return (
            db.query(Category)
            .filter(Category.section_id == section_id)
            .all()
        )

    @staticmethod
    def get_products_by_category(db: Session, category_id: int, limit: int = 5):
        return (
            db.query(Product)
            .options(joinedload(Product.variants))
            .filter(Product.category_id == category_id)
            .order_by(Product.id)
            .limit(limit)
            .all()
        )