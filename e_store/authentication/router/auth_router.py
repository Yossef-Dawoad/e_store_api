import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from e_store.authentication.hashing import verify_password
from e_store.authentication.jwt import authenticate_user, create_access_tok, get_current_active_user, get_user
from e_store.authentication.mail import VERIFY_ACCOUNT_CTX, send_welcome_verification_success_email
from e_store.authentication.schemas import TokenPublic, UserAccountVerify
from e_store.db import get_session
from e_store.shared.exceptions.http_400s import bad_400_excep, forbiden_403_excep, unauthorized_401_excep
from e_store.users.models.user import User, UserCreate, UserPublic
from e_store.users.services import create_new_user

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
    status_code=status.HTTP_201_CREATED,
    # callbacks=[]
)
async def create_user_acc(
    user: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
    background_tasks: BackgroundTasks,
) -> UserPublic:
    if await get_user(session, user.email):
        raise forbiden_403_excep(
            detail=f"User with email: {user.email} already exists",
        )
    return await create_new_user(user, session, background_tasks)


@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_user_account(
    data: UserAccountVerify,
    background_tasks: BackgroundTasks,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserPublic:
    if not (user := await get_user(session, data.email)):
        raise forbiden_403_excep(
            detail="This Verification Link is Not Valid",
        )
    verify_tok = user.create_hashed_ctx(VERIFY_ACCOUNT_CTX)
    try:
        is_valid_token = verify_password(verify_tok, data.token)
    except Exception as verify_excep:
        logging.exception(verify_excep)
        is_valid_token = False
    if not is_valid_token:
        raise bad_400_excep(detail="This Link either Expired or Not Valid")
    user.disabled = False
    user.updated_at = datetime.now(tz=timezone.utc)
    user.verified_at = datetime.now(tz=timezone.utc)
    session.add(user)
    await session.commit(user)
    await session.refresh(user)
    # TODO Sending Welcome Email Activatetion Success
    await send_welcome_verification_success_email(
        user=user,
        background_tasks=background_tasks,
    )
    return user


@router.get("/users/me/", response_model=UserPublic)
def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserPublic:
    return current_user
