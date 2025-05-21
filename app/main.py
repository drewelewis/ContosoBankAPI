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
    get_users,
    get_user_by_id
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

# Get all users
@app.post("/users/")
async def add_user(user_data:UserCreateModel, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    try:
        new_user:User = await create_user(db_session,user_data)
    except Exception as e:
        logger.exception(f"Error: {e}",stack_info=True)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    return new_user

#get user by id
@app.get("/users/{user_id}")
async def read_user(user_id: str, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    try:
        user = await get_user_by_id(db_session, user_id)
        if user is None:
            logger.error(f"User not found: user_id={user_id}")
            raise HTTPException(
                status_code=404, detail="User not found"
            )
    except Exception as e:
        logger.exception(f"Error: {e}",stack_info=True)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    return user

@app.get("/users/")
async def read_users(db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    try:
        users = await get_users(db_session)
        if users is None:
            raise HTTPException(
                status_code=404, detail="Users not found"
            )
    except Exception as e:
        logger.exception(f"Error: {e}",stack_info=True)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
    return users

