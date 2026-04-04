from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    VariantUpdate,
    VariantResponse
)
from app.schemas.pagination import CursorPage
from app.Service.product_service import ProductService
from app.dependencies.product_dependency import get_product_service

router = APIRouter(prefix="/products", tags=["Products"])


# ------------------------------------------------------------------ #
#  Product endpoints                                                   #
# ------------------------------------------------------------------ #

@router.post(
    "/",
    response_model=ProductResponse,
    summary="Create Product",
    description="Create a product with multiple variants"
)
def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    return service.create_product(product)


@router.get(
    "/",
    response_model=CursorPage[ProductResponse],
    summary="Get Products (Cursor Pagination)"
)
def get_products(
    cursor: Optional[str] = Query(None, description="Cursor for pagination"),
    limit: int = Query(10, ge=1, le=50),
    service: ProductService = Depends(get_product_service)
):
    return service.get_products(cursor, limit)


@router.get(
    "/category/{category_id}",
    response_model=CursorPage[ProductResponse],
    summary="Get Products by Category"
)
def get_products_by_category(
    category_id: int,
    cursor: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    service: ProductService = Depends(get_product_service)
):
    return service.get_products_by_category(category_id, cursor, limit)


@router.get(
    "/brand/{brand_id}",
    response_model=CursorPage[ProductResponse],
    summary="Get Products by Brand"
)
def get_products_by_brand(
    brand_id: int,
    cursor: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    service: ProductService = Depends(get_product_service)
):
    return service.get_products_by_brand(brand_id, cursor, limit)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get Single Product"
)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    return service.get_product(product_id)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update Product"
)
def update_product(
    product_id: int,
    updates: ProductUpdate,
    service: ProductService = Depends(get_product_service)
):
    return service.update_product(product_id, updates)


@router.delete(
    "/{product_id}",
    summary="Delete Product"
)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    return service.delete_product(product_id)


# ------------------------------------------------------------------ #
#  Variant endpoints                                                   #
# ------------------------------------------------------------------ #

@router.put(
    "/{product_id}/variants/{variant_id}",
    response_model=VariantResponse,
    summary="Update Product Variant"
)
def update_variant(
    product_id: int,
    variant_id: int,
    updates: VariantUpdate,
    service: ProductService = Depends(get_product_service)
):
    return service.update_variant(variant_id, updates)


@router.delete(
    "/{product_id}/variants/{variant_id}",
    summary="Delete Product Variant"
)
def delete_variant(
    product_id: int,
    variant_id: int,
    service: ProductService = Depends(get_product_service)
):
    return service.delete_variant(variant_id)