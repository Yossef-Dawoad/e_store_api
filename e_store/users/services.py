from e_store.users.models import User, UserCreate
from e_store.users.hashing import hash_password
from sqlmodel.ext.asyncio.session import AsyncSession


async def create_new_user(
    user: UserCreate,
    session: AsyncSession,
) -> User:
    hashed_password = hash_password(user.password)
    extra_data = {"hashed_password": hashed_password}
    new_user = User.model_validate(user, update=extra_data)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def update_existing_user(user: User, session: AsyncSession):
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
