from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from e_store.config import get_settings
from e_store.shared.exceptions.http_400s import bad_400_excep, unauthorized_401_excep
from e_store.users.hashing import verify_password
from e_store.users.models.user import User

from .schemas import TokenData

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.email == username)
    user = (await session.exec(stmt)).first()
    return user


async def authenticate_user(session: AsyncSession, username: str, password: str) -> bool | User:
    user = await get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_tok(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=[settings.algorithm])
    return encode_jwt


async def get_current_user(
    session: AsyncSession,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise unauthorized_401_excep(
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise unauthorized_401_excep(
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user(session, username=token_data.username)
    if user is None:
        raise unauthorized_401_excep(
            detail="Could not Find any User with this credentials",
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.disabled:
        raise bad_400_excep(detail="Inactive user")
    return current_user
