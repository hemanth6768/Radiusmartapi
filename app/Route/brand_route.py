from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.brand import BrandCreate, BrandUpdate, BrandResponse
from app.Service.brand_service import BrandService

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.post("/", response_model=BrandResponse)
def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    return BrandService.create_brand(db, brand)


@router.get("/", response_model=List[BrandResponse])
def get_brands(db: Session = Depends(get_db)):
    return BrandService.get_brands(db)


@router.get("/{brand_id}", response_model=BrandResponse)
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    return BrandService.get_brand(db, brand_id)


@router.put("/{brand_id}", response_model=BrandResponse)
def update_brand(brand_id: int, updates: BrandUpdate, db: Session = Depends(get_db)):
    return BrandService.update_brand(db, brand_id, updates)


@router.delete("/{brand_id}")
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    return BrandService.delete_brand(db, brand_id)