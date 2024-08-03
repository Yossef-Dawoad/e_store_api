import enum
import logging
import uuid
from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from e_store.config import get_settings
from e_store.db import get_session
from e_store.shared.exceptions.http_400s import bad_400_excep, unauthorized_401_excep
from e_store.users.hashing import verify_password
from e_store.users.models.user import User

from .schemas import TokenData

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

log = logging.getLogger("estore-logs")


# create an enum
class TokenTypes(str, enum.Enum):
    access = "access"
    refresh = "refresh"


async def get_user(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.email == username)
    return (await session.exec(stmt)).first()


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
    to_encode.update({"jti": str(uuid.uuid4())})  # JWT ID
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_tok(token: dict) -> dict | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except jwt.PyJWTError as auth_err:
        log.exception(auth_err)
        return None


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    try:
        payload = decode_tok(token)
        username = payload.get("sub")
        if username is None:
            raise unauthorized_401_excep(
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)
    except InvalidTokenError as err:
        raise unauthorized_401_excep(
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err
    user = await get_user(session, username=token_data.username)
    if user is None:
        raise unauthorized_401_excep(
            detail="Could not Find any User with this credentials",
        )
    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.disabled:
        raise bad_400_excep(detail="Inactive user")
    return current_user
