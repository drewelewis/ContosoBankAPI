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

async def create_user(db_session: AsyncSession,user_data:UserCreateModel) ->  User:
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

    return new_user

async def get_users(db_session: AsyncSession) -> list[User]:
    async with db_session as session:
        result = await session.execute(select(User).order_by(User.created_at.desc()))
        users = result.scalars().all()
    return users

