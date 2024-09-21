from datetime import datetime, timezone

from fastapi import BackgroundTasks
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.authentication.hashing import hash_password
from e_store.shared.exceptions.http_400s import not_found_404_excep
from e_store.users.models.user import User, UserCreate, UserUpdate


async def create_new_user(
    user: UserCreate,
    session: AsyncSession,
) -> User:
    # TODO check for password strengh
    hashed_password = hash_password(user.password)
    extra_data = {"hashed_password": hashed_password}
    new_user = User.model_validate(user, update=extra_data)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_email(email: str, session: AsyncSession) -> User:
    user = (await session.exec(select(User).where(User.email == email))).first()
    if not user:
        raise not_found_404_excep(detail=f"User with email {email} not found")
    return user
