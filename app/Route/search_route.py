from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductResponse

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/", response_model=list[ProductResponse])
def search_products(
    q: str = Query(..., min_length=1),
    limit: int = 10,
    db: Session = Depends(get_db)
):

    products = (
        db.query(Product)
        .options(
            joinedload(Product.variants),
            joinedload(Product.brand),
            joinedload(Product.category)
        )
        .filter(Product.is_active == True)
        .filter(Product.name.ilike(f"%{q}%"))   # PREFIX SEARCH
        .limit(limit)
        .all()
    )

    return products