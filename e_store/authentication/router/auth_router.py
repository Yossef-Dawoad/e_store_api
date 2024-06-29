from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from e_store.authentication.jwt import authenticate_user, create_access_tok, get_current_active_user, get_user
from e_store.authentication.schemas import TokenPublic
from e_store.db import get_session
from e_store.shared.exceptions.http_400s import forbiden_403_excep, unauthorized_401_excep
from e_store.users.models.user import User, UserCreate, UserPublic
from e_store.users.services import create_new_user

# TODO register the router in the app
router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signin", response_model=TokenPublic, status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TokenPublic:
    user_authenticated = await authenticate_user(session, form_data.username, form_data.password)
    if not user_authenticated:
        raise unauthorized_401_excep(
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_tok(data={"sub": form_data.username})  # TODO should be user.email ??
    refresh_token = create_access_tok(
        data={"sub": form_data.username},
        expires_delta=timedelta(days=3),
    )
    return TokenPublic(
        access_token=access_token,
        refresh_token=refresh_token,
        extra={"username": form_data.username, "uid": user_authenticated.id},
    )


@router.post(
    "/signup",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_acc(
    user: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserPublic:
    if await get_user(session, user.email):
        raise forbiden_403_excep(
            detail=f"User with email: {user.email} already exists",
        )
    return await create_new_user(user, session)


@router.get("/users/me/", response_model=UserPublic)
def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserPublic:
    return current_user
