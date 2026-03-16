from pydantic import BaseModel
from typing import List, Optional


class VariantPreview(BaseModel):
    id: int
    base_unit: str
    value: Optional[float]
    base_price: float
    stock_quantity: float
    image_url: Optional[str]

    class Config:
        from_attributes = True


class ProductPreview(BaseModel):
    id: int
    name: str
    image_url: Optional[str]
    variants: List[VariantPreview]

    class Config:
        from_attributes = True


class CategoryWithProducts(BaseModel):
    id: int
    name: str
    next_cursor: Optional[str]
    products: List[ProductPreview]

    class Config:
        from_attributes = True


class SectionWithCategories(BaseModel):
    id: int
    name: str
    categories: List[CategoryWithProducts]

    class Config:
        from_attributes = True


class HomeResponse(BaseModel):
    sections: List[SectionWithCategories]