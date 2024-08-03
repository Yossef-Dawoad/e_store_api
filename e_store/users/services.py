from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.users.hashing import hash_password
from e_store.users.models.user import User, UserCreate, UserUpdate


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
