from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.Repository.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.category import Category


class CategoryService:


    @staticmethod
    def create_category(db: Session, category: CategoryCreate):

        existing = CategoryRepository.get_by_name_and_section(
            db, category.name, category.section_id
        )

        if existing:
            raise HTTPException(status_code=400, detail="Category already exists in this section")

        return CategoryRepository.create(db, category)


    @staticmethod
    def get_categories(db: Session, section_id: int | None = None):

        if section_id:
            return CategoryRepository.get_by_section(db, section_id)

        return CategoryRepository.get_all(db)
    
    @staticmethod
    def get_sections_with_categories(db: Session):

      sections = CategoryRepository.get_sections_with_categories(db)

      if not sections:
        raise HTTPException(status_code=404, detail="No sections found")

      for section in sections:

        # Add static prefix for section image
          if section.image_url:
             section.image_url = f"/static/{section.image_url}"

          for category in section.categories:

            # Add static prefix for category image
             if category.image_url:
                 category.image_url = f"/static/{category.image_url}"

      return sections
    

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