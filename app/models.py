from sqlalchemy import ForeignKey, ForeignKeyConstraint, UniqueConstraint,Column, String, TIMESTAMP, ForeignKey, UUID
from sqlalchemy.orm import (DeclarativeBase,Mapped,mapped_column,relationship)
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.dialects.postgresql import UUID as pgUUID  

from datetime import datetime  
import uuid 

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=datetime.now)  
    updated_at: Mapped[datetime | None] = mapped_column(TIMESTAMP)  
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP)

class PydanticBaseModel(BaseModel):
    pass

# Users Model  
class User(Base):  
    __tablename__ = "users" 
    user_id: Mapped[uuid.UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)  
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)  
    email: Mapped[str] = mapped_column(String(100), nullable=False)  
    username: Mapped[str] = mapped_column(String(100), nullable=False)  
    password_hash: Mapped[str] = mapped_column(String(150), nullable=False)  

class UserCreateModel(PydanticBaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password_hash: str

