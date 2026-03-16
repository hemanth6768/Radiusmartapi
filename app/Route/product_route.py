from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional , List

from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.pagination import CursorPage
from app.Service.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


# Create product with variants
@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return ProductService.create_product(db, product)

@router.post("/bulk", response_model=List[ProductResponse])
def create_products(products: List[ProductCreate], db: Session = Depends(get_db)):
    return ProductService.create_products_bulk(db, products)


# Cursor paginated product listing
@router.get("/", response_model=CursorPage[ProductResponse])
def get_products(
    cursor: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    return ProductService.get_products(db, cursor, limit)


# Get single product
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService.get_product(db, product_id)


# Products by category with cursor pagination
@router.get("/category/{category_id}", response_model=CursorPage[ProductResponse])
def get_products_by_category(
    category_id: int,
    cursor: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    return ProductService.get_products_by_category(db, category_id, cursor, limit)


# Products by brand
@router.get("/brand/{brand_id}", response_model=CursorPage[ProductResponse])
def get_products_by_brand(
    brand_id: int,
    cursor: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    return ProductService.get_products_by_brand(db, brand_id, cursor, limit)


# Update product
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updates: ProductUpdate, db: Session = Depends(get_db)):
    return ProductService.update_product(db, product_id, updates)


# Delete product
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService.delete_product(db, product_id)