from fastapi import APIRouter, Depends
from typing import List

from app.schemas.brand import BrandCreate, BrandUpdate, BrandResponse
from app.Service.brand_service import BrandService
from app.dependencies.brand_dependency import get_brand_service


router = APIRouter(prefix="/brands", tags=["Brands"])


@router.post("/", response_model=BrandResponse)
def create_brand(
    brand: BrandCreate,
    service: BrandService = Depends(get_brand_service)
):
    return service.create_brand(brand)


@router.get("/", response_model=List[BrandResponse])
def get_brands(
    service: BrandService = Depends(get_brand_service)
):
    return service.get_brands()


@router.get("/{brand_id}", response_model=BrandResponse)
def get_brand(
    brand_id: int,
    service: BrandService = Depends(get_brand_service)
):
    return service.get_brand(brand_id)


@router.put("/{brand_id}", response_model=BrandResponse)
def update_brand(
    brand_id: int,
    updates: BrandUpdate,
    service: BrandService = Depends(get_brand_service)
):
    return service.update_brand(brand_id, updates)


@router.delete("/{brand_id}")
def delete_brand(
    brand_id: int,
    service: BrandService = Depends(get_brand_service)
):
    return service.delete_brand(brand_id)