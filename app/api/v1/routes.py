from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.db.deps import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import register_user
from app.repositories.user_repo import get_by_email

from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.deps import get_current_user
from app.core.config import settings
from app.models.user import User

router = APIRouter()


@router.post("/users", response_model=UserOut)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await register_user(
        db,
        payload.email,
        payload.password,
        payload.first_name,
        payload.last_name,
        payload.phone
    )
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")

    return user


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_by_email(db, payload.email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not await verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token({"sub": user.email})
    refresh = create_refresh_token({"sub": user.email})

    return {"access_token": access, "refresh_token": refresh}


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest):
    try:
        data = jwt.decode(
            payload.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if data.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        email = data.get("sub")

        new_access = create_access_token({"sub": email})
        new_refresh = create_refresh_token({"sub": email})

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout")
async def logout():
    return {"message": "Client should delete tokens"}


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
