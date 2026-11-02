from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import final, override

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import AppSettings


class Database(ABC):
    def __init__(self):
        self.async_sessionmaker: async_sessionmaker[AsyncSession] | None = None
        self.async_engine: AsyncEngine | None = None

    async def __call__(self) -> AsyncIterator[AsyncSession]:
        """For use with FastAPI Depends"""
        if not self.async_sessionmaker:
            raise ValueError("async_sessionmaker not available. Run setup() first.")
        if not self.async_engine:
            raise ValueError("async_engine not available. Run setup() first.")
        async with self.async_sessionmaker() as session:
            yield session

    @abstractmethod
    def setup(self, config: AppSettings) -> None: ...

    @abstractmethod
    async def shutdown(self) -> None: ...


@final
class PostgresDatabase(Database):
    @override
    def setup(self, config: AppSettings) -> None:
        url_object = URL.create(
            config.dialect,
            username=config.db_user,
            password=config.db_password.get_secret_value(),
            host=config.db_host,
            database=config.db_name,
            port=config.db_port,
        )
        self.async_engine = create_async_engine(
            url_object,
            echo=config.sql_command_echo,
        )
        self.async_sessionmaker = async_sessionmaker(
            self.async_engine, class_=AsyncSession
        )

    @override
    async def shutdown(self) -> None:
        if self.async_engine:
            await self.async_engine.dispose()


database = PostgresDatabase()
