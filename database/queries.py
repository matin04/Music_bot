from sqlalchemy import select
from sqlalchemy import func

from database.database import (
    async_session,
    engine,
    Base
)

from database.models import (
    User,
    Download
)


async def create_tables():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )


async def add_user(user_id: int):

    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                User.user_id == user_id
            )
        )

        user = result.scalar()

        if not user:

            session.add(
                User(user_id=user_id)
            )

            await session.commit()

async def add_download(
    user_id: int,
    query: str
):

    async with async_session() as session:

        session.add(
            Download(
                user_id=user_id,
                query=query
            )
        )

        await session.commit()


async def get_total_users():

    async with async_session() as session:

        result = await session.execute(
            select(func.count(User.id))
        )

        return result.scalar()

async def get_total_downloads():

    async with async_session() as session:

        result = await session.execute(
            select(func.count(Download.id))
        )

        return result.scalar()