from asyncio import to_thread
from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt
from app.core.config import settings


async def hash_password(password: str) -> str:
    hashed = await to_thread(bcrypt.hashpw, password.encode(), bcrypt.gensalt())
    return hashed.decode()


async def verify_password(password: str, hashed: str) -> bool:
    return await to_thread(bcrypt.checkpw, password.encode(), hashed.encode())


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
