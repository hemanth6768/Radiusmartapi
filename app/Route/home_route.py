from fastapi import APIRouter, Depends
from app.schemas.home import HomeResponse
from app.Service.home_service import HomeService
from app.dependencies.home_dependency import get_home_service


router = APIRouter(prefix="/home", tags=["Home"])


@router.get(
    "/",
    response_model=HomeResponse,
    summary="Get Home Page Data",
    description=(
        "Returns all sections → categories → first 5 products per category. "
        "Each category includes a `next_cursor` — pass it to "
        "GET /home/category/{id}/products?cursor=xxx to load more products."
    )
)
def get_home(
    service: HomeService = Depends(get_home_service)
):
    return service.get_home_data()