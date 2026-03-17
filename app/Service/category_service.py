from fastapi import HTTPException
from app.Repository.category_repository import CategoryRepository
from app.core.logger import logger


class CategoryService:

    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    def create_category(self, category):
        existing = self.repo.get_by_name_and_section(
            category.name, category.section_id
        )

        if existing:
            logger.warning(
                f"Duplicate category: {category.name} in section {category.section_id}"
            )
            raise HTTPException(
                status_code=400,
                detail="Category already exists in this section"
            )

        return self.repo.create(category)

    def get_categories(self, section_id: int | None = None):
        if section_id:
            return self.repo.get_by_section(section_id)

        return self.repo.get_all()

    def get_category(self, category_id: int):
        category = self.repo.get_by_id(category_id)

        if not category:
            logger.warning(f"Category not found id={category_id}")
            raise HTTPException(status_code=404, detail="Category not found")

        return category

    def get_sections_with_categories(self):
        sections = self.repo.get_sections_with_categories()

        if not sections:
            logger.warning("No sections found")
            raise HTTPException(status_code=404, detail="No sections found")

        # Add static path
        for section in sections:
            if section.image_url:
                section.image_url = f"/static/{section.image_url}"

            for category in section.categories:
                if category.image_url:
                    category.image_url = f"/static/{category.image_url}"

        return sections

    def update_category(self, category_id: int, updates):
        category = self.repo.get_by_id(category_id)

        if not category:
            logger.warning(f"Update failed, category not found id={category_id}")
            raise HTTPException(status_code=404, detail="Category not found")

        return self.repo.update(category, updates)

    def delete_category(self, category_id: int):
        category = self.repo.get_by_id(category_id)

        if not category:
            logger.warning(f"Delete failed, category not found id={category_id}")
            raise HTTPException(status_code=404, detail="Category not found")

        self.repo.delete(category)

        return {"message": "Category deleted successfully"}