from pydantic import BaseModel
from typing import List, Optional
from app.models.enums import ProductCategory


class ProductImageOut(BaseModel):
    id: int
    url: str

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    price: int
    description: Optional[str] = None
    category: ProductCategory
    definition: Optional[str] = None


class ProductOut(BaseModel):
    id: int
    name: str
    price: int
    description: Optional[str]
    category: ProductCategory
    definition: Optional[str]
    updated_at: str
    images: List[ProductImageOut]

    class Config:
        from_attributes = True
