from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from app.config import config

from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = config.DATABASE_URL


def get_engine():
    try:
        return create_async_engine(
            SQLALCHEMY_DATABASE_URL, echo=True
        )
    except Exception as e:
        print(e)
        return None


# sessionmaker for async sessions
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_engine(),
    class_=AsyncSession,
)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
