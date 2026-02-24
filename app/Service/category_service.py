from sqlalchemy.orm import Session
from app.Repository.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from fastapi import HTTPException
from app.models.category import Category

class CategoryService:

    @staticmethod
    def create_category(db, category):

        # Check if category already exists
        existing = db.query(Category).filter(Category.name == category.name).first()

        if existing:
            raise HTTPException(status_code=400, detail="Category already exists")

        return CategoryRepository.create(db, category)
    

    @staticmethod
    def get_categories(db: Session):
        return CategoryRepository.get_all(db)

    @staticmethod
    def get_category(db: Session, category_id: int):
        category = CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    @staticmethod
    def update_category(db: Session, category_id: int, updates: CategoryUpdate):

        category = CategoryRepository.get_by_id(db, category_id)

        if not category:
          raise HTTPException(status_code=404, detail="Category not found")

        return CategoryRepository.update(db, category, updates)

    @staticmethod
    def delete_category(db: Session, category_id: int):
        category = CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        CategoryRepository.delete(db, category)
        return {"message": "Category deleted successfully"}