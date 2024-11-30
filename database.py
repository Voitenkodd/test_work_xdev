from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm.decl_api import DeclarativeMeta


class Database:

    __instance = None

    def __new__(cls, host: str, engine_kwargs: dict[str, Any] = {}) -> "Database":
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__new__(cls)
            cls.__instance.db_url = host
            cls.__instance.__engine = create_async_engine(host, **engine_kwargs)
            cls.__instance.__session_local = async_sessionmaker(
                bind=cls.__instance._engine, expire_on_commit=False
            )

        return cls.__instance

    @property
    def _engine(self):
        return self.__engine

    @property
    def _session_local(self):
        return self.__session_local

    async def close(self):
        await self._engine.dispose()
        self.__instance = None

    async def init_db(self, base: DeclarativeMeta):
        async with self._engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        async with self._session_local() as session:
            try:
                yield session
            except SQLAlchemyError as e:
                # todo добавить логирование
                raise e
