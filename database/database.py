from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = (
    "postgresql+asyncpg://postgres:55055904855@localhost/music_bot"
)


engine = create_async_engine(
    DATABASE_URL,
    echo=False
)


async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass