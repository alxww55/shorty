from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from .config import settings


class DatabaseHelper:
    def __init__(self):
        self.engine = create_async_engine(
            url=str(settings.database_url), echo=settings.debug
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False
        )

    async def session_dependency(self) -> AsyncGenerator:
        async with self.session_factory() as session:
            yield session
            await session.close()


db_helper = DatabaseHelper()
