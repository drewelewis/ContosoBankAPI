from sqlalchemy import (
    and_,
    delete,
    select,
    text,
    update,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, load_only

from app.models import (
    User,
    UserCreateModel
)
import bcrypt

from app.logger import logger

async def create_user(db_session: AsyncSession, user_data: UserCreateModel) -> User:
    try:
        new_user = User()
        new_user.first_name = user_data.first_name
        new_user.last_name = user_data.last_name
        new_user.email = user_data.email
        new_user.username = user_data.username
        # Hash the password securely
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user_data.password_hash.encode('utf-8'), salt)
        new_user.password_hash = hashed_password.decode('utf-8')
        async with db_session.begin():
            db_session.add(new_user)
            await db_session.flush()
            user_id = new_user.user_id
            await db_session.commit()
    except Exception as e:
        logger.exception(f"[operations.create_user] Error: {e}")
        new_user = None   
    return new_user

async def get_users(db_session: AsyncSession) -> list[User]:
    try:
        async with db_session as session:
            result = await session.execute(select(User).order_by(User.created_at.desc()))
            users = result.scalars().all()
    except Exception as e:
        logger.exception(f"[operations.get_users] Error: {e}")
        users = None
    return users

async def get_user_by_id(db_session: AsyncSession, user_id: str) -> list[User] | None:
    try:
        query = (select(User)
            .where(User.user_id == user_id)
        )
        async with db_session as session:
            result = await session.execute(query)
            user = result.scalars().first()
    except Exception as e:
        logger.exception(f"[operations.get_user_by_id] Error: {e}")
        user = None
    return user

