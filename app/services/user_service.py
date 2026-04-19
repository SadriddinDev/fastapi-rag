from app.repositories.user_repo import get_by_email, create
from app.core.security import hash_password
from app.models.user import User


async def register_user(
    db,
    email: str,
    password: str,
    first_name: str | None = None,
    last_name: str | None = None,
    phone: str | None = None
):
    existing = await get_by_email(db, email)
    if existing:
        return None

    user = User(
        email=email,
        hashed_password=await hash_password(password),
        first_name=first_name,
        last_name=last_name,
        phone=phone,
    )

    return await create(db, user)
