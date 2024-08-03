from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.db import get_session
from e_store.users.models.user import User, UserPublic, UserUpdate

router = APIRouter(tags=["Users"], prefix="/users")


@router.get("/", response_model=list[UserPublic])
async def read_users(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    stmt = select(User).offset(offset).limit(limit)
    return (await session.exec(stmt)).all()


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
    curr_user = await session.get(User, user_id)
    if not curr_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_update_data = user.model_dump(exclude_unset=True)
    curr_user.sqlmodel_update(user_update_data)
    session.add(curr_user)
    await session.commit()
    await session.refresh(curr_user)

    return curr_user


@router.delete("/{user_id}", status_code=204)
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
