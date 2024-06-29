from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from e_store.config import get_settings
from e_store.db import get_session, init_db
from main import app

settings = get_settings()


# the engine is the starting point for all the SQLModel operations
async_engine = create_async_engine(
    url=settings.test_database_url,
    echo=True,
)

# TODO Initailze the database calling the async `init_db`


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    """
    InOrder to interact with the database, we need to create a session.
    Yield a new session.
    """
    async_session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = get_test_session
