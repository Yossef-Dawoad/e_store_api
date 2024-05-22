from typing import AsyncGenerator
from sqlmodel import SQLModel

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.orm import sessionmaker
from e_store.config import get_settings


# the engine is the starting point for all the SQLModel operations
async_engine = create_async_engine(
    url=get_settings.database_url,
    echo=True,
)


async def init_db():
    async with async_engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
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
