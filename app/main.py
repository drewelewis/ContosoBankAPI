from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus

from app.models import Base, User, UserCreateModel
from app.database import get_db_session, get_engine
from app.operations import (
    create_user,
    get_users
)

from app.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)


@app.post("/users/")
async def add_user(user_data:UserCreateModel, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    logger.info(f"Creating user with data: {user_data}")
    new_user:User = await create_user(db_session,user_data)
    return new_user

@app.get("/users/")
async def read_users(db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    logger.info(f"Creating user with data")
    users = await get_users(db_session)
    if users is None:
        raise HTTPException(
            status_code=404, detail="Ticket not found"
        )
    return users

