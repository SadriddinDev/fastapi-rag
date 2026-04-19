from app.models.product import Product
from app.repositories.product_repo import create, get_all, get_by_id


async def create_product(db, data, user_id: int):
    product = Product(
        **data.model_dump(),
        user_id=user_id
    )
    return await create(db, product)


async def list_products(db):
    return await get_all(db)


async def get_product(db, product_id: int):
    return await get_by_id(db, product_id)
