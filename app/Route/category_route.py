from fastapi import APIRouter, Depends ,Query
from sqlalchemy.orm import Session
from typing import List ,  Optional

from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse,SectionWithCategories
from app.Service.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


# Create a new category
# Example: Dairy, Fruits, Beverages etc.
@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return CategoryService.create_category(db, category)


# Get all categories
# Optional: filter categories by section_id
# Example: /categories?section_id=1
@router.get("/", response_model=List[CategoryResponse])
def get_categories_bysection(
    section_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    return CategoryService.get_categories(db, section_id)

# Get all categories
# Used when UI needs full category list
@router.get("/all", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return CategoryService.get_categories(db)

# Get all sections with their categories
# Used for homepage category navigation
@router.get("/sections", response_model=List[SectionWithCategories])
def get_sections_with_categories(db: Session = Depends(get_db)):
    return CategoryService.get_sections_with_categories(db)

# Get a single category by its ID
# Example: /categories/3
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return CategoryService.get_category(db, category_id)


# Update an existing category
# Example: change name, description, image, or section
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, updates: CategoryUpdate, db: Session = Depends(get_db)):
    return CategoryService.update_category(db, category_id, updates)


# Delete a category
# This removes the category from the database
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return CategoryService.delete_category(db, category_id)