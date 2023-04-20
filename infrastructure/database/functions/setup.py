from typing import Callable, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from infrastructure.database.models import BaseModel
from tgbot.config import DatabaseConfig


async def create_session_pool(
        db: DatabaseConfig, echo: bool = False, drop_all_tables: bool = False
) -> Callable[[], AsyncContextManager[AsyncSession]]:
    engine = create_async_engine(url=db.construct_sqlalchemy_url(), echo=echo)  # Building an asynchronous engine

    async with engine.begin() as connection:
        # Synchronization tables
        if drop_all_tables:
            await connection.run_sync(BaseModel.metadata.drop_all)  # Deleting all used tables
        await connection.run_sync(BaseModel.metadata.create_all)  # Creation of all used tables

    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool
