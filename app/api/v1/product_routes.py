from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.core.deps import get_current_user
from app.schemas.product import ProductCreate, ProductOut
from app.services.product_service import create_product, list_products, get_product
from app.models.user import User

router = APIRouter(tags=["Products"], dependencies=[Depends(get_current_user)])


@router.post("/", response_model=ProductOut)
async def create(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await create_product(db, payload, user.id)


@router.get("/", response_model=list[ProductOut])
async def list_all(db: AsyncSession = Depends(get_db)):
    return await list_products(db)


@router.get("/{product_id}", response_model=ProductOut)
async def detail(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Not found")

    return product
