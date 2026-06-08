from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenPair

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenPair, status_code=201)
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_session)) -> TokenPair:
    existing = await session.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=payload.email, name=payload.name, password_hash=hash_password(payload.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return TokenPair(access_token=create_access_token(user), refresh_token=create_refresh_token(user))


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)) -> TokenPair:
    result = await session.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return TokenPair(access_token=create_access_token(user), refresh_token=create_refresh_token(user))


@router.post("/refresh", response_model=TokenPair)
async def refresh(refresh_token: str, session: AsyncSession = Depends(get_session)) -> TokenPair:
    settings = get_settings()
    try:
        payload = jwt.decode(refresh_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != "refresh":
            raise ValueError("invalid token type")
        user_id = int(payload["sub"])
    except (JWTError, ValueError, KeyError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    return TokenPair(access_token=create_access_token(user), refresh_token=create_refresh_token(user))
