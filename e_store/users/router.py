from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.db import get_session
from e_store.users.models import User, UserCreate, UserPublic, UserUpdate
from e_store.users.services import create_new_user, update_existing_user
from e_store.users.validator import verify_email_exists

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", response_model=UserPublic, status_code=201)
async def create_user(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    user: UserCreate,
):
    user_exists = await verify_email_exists(user.email, session)
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="User with this mail Already exists.",
        )
    db_user = await create_new_user(user, session)
    return db_user


@router.get("/", response_model=list[UserPublic])
async def read_users(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    stmt = select(User).offset(offset).limit(limit)
    users = (await session.exec(stmt)).all()
    return users


@router.get("/{user_id}", response_model=UserPublic)
async def read_user(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    user_id: int,
):
    if not (user := await session.get(User, user_id)):
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserPublic)
async def update_user(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    user_id: int,
    user: UserUpdate,
):
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user = await update_existing_user(user, session)
    return db_user


@router.delete("/{user_id}")
async def delete_user(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    user_id: int,
):
    if not (user := await session.get(User, user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    await session.delete(user)
    await session.commit()
    return {"ok": True}
