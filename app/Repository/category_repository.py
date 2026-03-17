from sqlalchemy.orm import Session, joinedload
from app.models.category import Category
from app.models.section import Section
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.core.logger import logger


class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, category: CategoryCreate):
        try:
            db_category = Category(**category.model_dump())

            self.db.add(db_category)
            self.db.commit()
            self.db.refresh(db_category)

            logger.info(f"Category created id={db_category.id}")
            return db_category

        except Exception as e:
            logger.error(f"Error creating category: {str(e)}")
            self.db.rollback()
            raise

    def get_all(self):
        return (
            self.db.query(Category)
            .filter(Category.is_active == True)
            .order_by(Category.id)
            .all()
        )

    def get_by_id(self, category_id: int):
        return (
            self.db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    def get_by_section(self, section_id: int):
        return (
            self.db.query(Category)
            .filter(
                Category.section_id == section_id,
                Category.is_active == True
            )
            .all()
        )

    def get_by_name_and_section(self, name: str, section_id: int):
        return (
            self.db.query(Category)
            .filter(
                Category.name == name,
                Category.section_id == section_id
            )
            .first()
        )

    def get_sections_with_categories(self):
        return (
            self.db.query(Section)
            .options(joinedload(Section.categories))
            .filter(Section.is_active == True)
            .order_by(Section.display_order)
            .all()
        )

    def update(self, db_category: Category, updates: CategoryUpdate):
        try:
            update_data = updates.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(db_category, key, value)

            self.db.commit()
            self.db.refresh(db_category)

            logger.info(f"Category updated id={db_category.id}")
            return db_category

        except Exception as e:
            logger.error(f"Error updating category: {str(e)}")
            self.db.rollback()
            raise

    def delete(self, db_category: Category):
        try:
            # ✅ Soft delete (recommended)
            db_category.is_active = False
            self.db.commit()

            logger.info(f"Category deleted id={db_category.id}")
            return db_category

        except Exception as e:
            logger.error(f"Error deleting category: {str(e)}")
            self.db.rollback()
            raise