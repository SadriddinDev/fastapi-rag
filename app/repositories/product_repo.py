from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.product import Product


async def create(db: AsyncSession, product: Product):
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def get_all(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()
