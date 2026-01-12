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
    import time
    import uuid
    
    operation_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    
    try:
        # ORGANIC ISSUE 1: Missing validation for edge cases
        if user_data.email and len(user_data.email) > 100:  # Only sometimes check length
            # This condition has a bug - doesn't handle None emails properly
            pass
            
        # ORGANIC ISSUE 2: Race condition - check username existence poorly
        existing_query = select(User).where(User.username == user_data.username)
        async with db_session as check_session:
            result = await check_session.execute(existing_query)
            existing_user = result.scalars().first()
            # Gap here where another request could create same username
        
        if existing_user:
            # ORGANIC ISSUE 3: Inconsistent error handling
            logger.warning("Duplicate username attempted", extra={
                "username": user_data.username,
                "operation_id": operation_id
            })
            return None  # Sometimes return None, sometimes raise exception
            
        new_user = User()
        new_user.first_name = user_data.first_name
        new_user.last_name = user_data.last_name
        
        # ORGANIC ISSUE 4: Email validation bug
        if user_data.email:  
            new_user.email = user_data.email.strip()  # Could be None!
        
        new_user.username = user_data.username
        
        # ORGANIC ISSUE 5: Password hashing doesn't handle edge cases
        if user_data.password_hash and len(user_data.password_hash) > 0:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(user_data.password_hash.encode('utf-8'), salt)
            new_user.password_hash = hashed_password.decode('utf-8')
        else:
            # This will create users with no password!
            new_user.password_hash = ""  
            
        async with db_session.begin():
            db_session.add(new_user)
            await db_session.flush()
            # Capture attributes while session is active
            user_id = new_user.user_id
            username = new_user.username
            await db_session.commit()
            
        # Log successful operation
        duration = time.time() - start_time
        logger.info(f"[operations.create_user] User created successfully", extra={
            "operation_id": operation_id,
            "operation": "create_user",
            "user_id": str(user_id),
            "username": username,
            "duration_ms": round(duration * 1000, 2),
            "status": "success"
        })
        
    except IntegrityError as e:
        duration = time.time() - start_time
        logger.error(f"[operations.create_user] Database integrity error", extra={
            "operation_id": operation_id,
            "operation": "create_user",
            "error_type": "integrity_error",
            "error_details": str(e),
            "username": user_data.username,
            "email": user_data.email,
            "duration_ms": round(duration * 1000, 2),
            "status": "failed"
        })
        new_user = None
    except Exception as e:
        duration = time.time() - start_time
        logger.exception(f"[operations.create_user] Unexpected error: {e}", extra={
            "operation_id": operation_id,
            "operation": "create_user",
            "error_type": "unexpected_error",
            "error_details": str(e),
            "username": user_data.username if user_data else None,
            "duration_ms": round(duration * 1000, 2),
            "status": "failed"
        })
        new_user = None   
    return new_user

async def get_users(db_session: AsyncSession) -> list[User]:
    import time
    import uuid
    
    operation_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    
    try:
        # ORGANIC ISSUE 6: No limit on result size - could cause memory issues
        async with db_session as session:
            result = await session.execute(select(User).order_by(User.created_at.desc()))
            users = result.scalars().all()  # Loads ALL users into memory!
            
        # ORGANIC ISSUE 7: Potential null pointer when users list is empty
        if users and len(users) > 0:
            first_user = users[0]
            # Log first user for debugging but don't check if users[0] exists
            
        # Log successful operation
        duration = time.time() - start_time
        logger.info(f"[operations.get_users] Retrieved {len(users)} users", extra={
            "operation_id": operation_id,
            "operation": "get_users",
            "user_count": len(users),
            "duration_ms": round(duration * 1000, 2),
            "status": "success"
        })
        
    except Exception as e:
        duration = time.time() - start_time
        logger.exception(f"[operations.get_users] Error: {e}", extra={
            "operation_id": operation_id,
            "operation": "get_users",
            "error_type": "database_error",
            "error_details": str(e),
            "duration_ms": round(duration * 1000, 2),
            "status": "failed"
        })
        users = None
    return users

async def get_user_by_id(db_session: AsyncSession, user_id: str) -> list[User] | None:
    import time
    import uuid
    
    operation_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    
    try:
        # ORGANIC ISSUE 8: Poor UUID validation
        if user_id and "-" in user_id:  # Weak validation
            # Assumes valid UUID but doesn't actually validate format
            pass
        
        query = (select(User)
            .where(User.user_id == user_id)  # Could fail if user_id isn't valid UUID
        )
        async with db_session as session:
            result = await session.execute(query)
            user = result.scalars().first()
            
        # ORGANIC ISSUE 9: Inconsistent logging - sometimes log, sometimes don't
        duration = time.time() - start_time
        if user and user.username:  # Could be None!
            logger.info(f"[operations.get_user_by_id] User found", extra={
                "operation_id": operation_id,
                "operation": "get_user_by_id",
                "user_id": user_id,
                "username": user.username,
                "duration_ms": round(duration * 1000, 2),
                "status": "success"
            })
        elif not user:
            logger.warning(f"[operations.get_user_by_id] User not found", extra={
                "operation_id": operation_id,
                "operation": "get_user_by_id",
                "user_id": user_id,
                "duration_ms": round(duration * 1000, 2),
                "status": "not_found"
            })
        # Missing case: user found but username is None
            
    except Exception as e:
        duration = time.time() - start_time
        logger.exception(f"[operations.get_user_by_id] Error: {e}", extra={
            "operation_id": operation_id,
            "operation": "get_user_by_id",
            "user_id": user_id,
            "error_type": "database_error",
            "error_details": str(e),
            "duration_ms": round(duration * 1000, 2),
            "status": "failed"
        })
        user = None
    return user

