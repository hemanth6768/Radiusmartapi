from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.Service.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/addproduct", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return ProductService.create_product(db, product)


@router.get("/allproducts", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return ProductService.get_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService.get_product(db, product_id)



@router.put("/updateproduct/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updates: ProductUpdate, db: Session = Depends(get_db)):
    return ProductService.update_product(db, product_id, updates)


@router.delete("/deleteproduct/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService.delete_product(db, product_id)


@router.get("/{category_id}/products", response_model=List[ProductResponse])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    return ProductService.get_products_by_category(db, category_id)