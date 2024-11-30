import datetime
import logging
import os
from functools import wraps

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession

from database import Database


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str

    debug: bool = True
    origins: list[str] = ["*"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db = Database(self.__db_url, engine_kwargs={"echo": True})

    @property
    def db(self) -> Database:
        return self._db

    @property
    def __db_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}/{self.postgres_db}"


class Logger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = os.path.abspath(log_dir)
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
        self._log_format = (
            "%(asctime)s - [%(levelname)s] - %(name)s - "
            "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
        )

        os.makedirs(self.log_dir, exist_ok=True)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self._add_file_handler(logging.INFO)
        self._add_file_handler(logging.WARNING)

    def _add_file_handler(self, level: int):
        log_file = os.path.join(self.log_dir, f"logger_{self.date}.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(self._log_format))
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

logger = Logger().get_logger()


def db_handler(func):
    @wraps(func)
    async def wrapper(self, db: AsyncSession, *args, **kwargs):
        try:
            return await func(self, db, *args, **kwargs)
        except Exception as e:
            await db.rollback()
            raise Exception(str(e))

    return wrapper


async def exception_handler(request: Request, exc: Exception):
    logger.error(f"{exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
