import asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String

from app.config import config
from app.models import UserCreateModel
from app.database import get_engine,get_db_session
from app.operations import (
    create_user

)
# Create an asynchronous engine
settings = config
DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)
fake=Faker()

# Create an asynchronous session factory
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def main():
    async with async_session() as session:
        for _ in range(200):
                user=await create_user(session, UserCreateModel(first_name=fake.first_name(), last_name=fake.last_name(), email=fake.email(), username=fake.user_name(), password_hash=fake.password()))

if __name__ == "__main__":
    asyncio.run(main())