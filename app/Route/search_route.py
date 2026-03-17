from fastapi import APIRouter, Depends, Query
from typing import List

from app.schemas.product import ProductResponse
from app.Service.search_service import SearchService
from app.dependencies.search_dependency import get_search_service


router = APIRouter(prefix="/search", tags=["Search"])


@router.get(
    "/",
    response_model=List[ProductResponse],
    summary="Search Products",
    description="Search products by name using partial match"
)
def search_products(
    q: str = Query(..., min_length=1, description="Search keyword"),
    limit: int = Query(10, ge=1, le=50),
    service: SearchService = Depends(get_search_service)
):
    return service.search_products(q, limit)