from datetime import datetime, timezone

from fastapi.background import BackgroundTasks
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.authentication.hashing import hash_password
from e_store.authentication.mail import send_request_verification_email
from e_store.authentication.security import verify_pass_strenth
from e_store.shared.exceptions.http_400s import bad_400_excep, not_found_404_excep
from e_store.users.models.user import User, UserCreate


async def create_new_user(
    user: UserCreate,
    session: AsyncSession,
    background_tasks: BackgroundTasks,
) -> User:
    if not verify_pass_strenth(user.password):
        raise bad_400_excep(
            detail="please include in your password digits, lower and upper charachters as well as special charachters like (@, %, &, *, ...)"
        )
    hashed_password = hash_password(user.password)
    extra_data = {
        "hashed_password": hashed_password,
        "updated_at": datetime.now(tz=timezone.utc),
    }
    # user.updated_at =

    new_user = User.model_validate(user, update=extra_data)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    # !TODO Send a verification main to the user
    # !TODO BackgroundTasks should be passed with route param!!!
    await send_request_verification_email(
        user=new_user,
        background_tasks=background_tasks,
    )
    return new_user


async def get_user_by_email(email: str, session: AsyncSession) -> User:
    user = (await session.exec(select(User).where(User.email == email))).first()
    if not user:
        raise not_found_404_excep(detail=f"User with email {email} not found")
    return user
