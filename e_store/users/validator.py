from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.users.models import User


async def verify_email_exists(email: str, session: AsyncSession) -> User | None:
    stmt = select(User).where(User.email == email)
    return (await session.exec(stmt)).first()
