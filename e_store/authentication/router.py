from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from e_store.authentication.jwt import authenticate_user, create_access_tok, get_current_active_user
from e_store.db import get_session
from e_store.shared.exceptions.http_400s import unauthorized_401_excep
from e_store.users.models.user import User, UserPublic

from .schemas import Token

router = APIRouter(tags=["authentication"])


@router.post("/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise unauthorized_401_excep(
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_tok(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserPublic:
    return current_user
