from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    SectionWithCategories,
    CursorPage,
)
from app.Service.category_service import CategoryService
from app.dependencies.category_dependency import get_category_service


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    return service.create_category(category)


@router.get("/", response_model=CursorPage[CategoryResponse])
def get_categories(
    section_id: Optional[int] = Query(None),
    cursor: Optional[str] = Query(None, description="Pagination cursor from previous response"),
    limit: int = Query(10, ge=1, le=100),
    service: CategoryService = Depends(get_category_service),
):
    return service.get_categories(section_id, cursor, limit)


@router.get("/all", response_model=CursorPage[CategoryResponse])
def get_all_categories(
    cursor: Optional[str] = Query(None, description="Pagination cursor from previous response"),
    limit: int = Query(10, ge=1, le=100),
    service: CategoryService = Depends(get_category_service),
):
    return service.get_categories(None, cursor, limit)


@router.get("/sections", response_model=CursorPage[SectionWithCategories])
def get_sections_with_categories(
    cursor: Optional[str] = Query(None, description="Pagination cursor from previous response"),
    limit: int = Query(10, ge=1, le=100),
    service: CategoryService = Depends(get_category_service),
):
    return service.get_sections_with_categories(cursor, limit)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
):
    return service.get_category(category_id)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    updates: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    return service.update_category(category_id, updates)


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
):
    return service.delete_category(category_id)