from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:

    @staticmethod
    def create(db: Session, category: CategoryCreate):
        db_category = Category(**category.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def get_all(db: Session):
        return db.query(Category).all()

    @staticmethod
    def get_by_id(db: Session, category_id: int):
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def update(db: Session, db_category: Category, updates: CategoryUpdate):
        update_data = updates.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def delete(db: Session, db_category: Category):
        db.delete(db_category)
        db.commit()