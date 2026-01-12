#!/usr/bin/env python3
"""
Database creation script for ContosoBankAPI
This script creates the database if it doesn't exist, then creates all tables and indexes.
"""
import asyncio
import sys
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import ProgrammingError
import asyncpg

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_engine
from app.models import Base
from app.logger import logger
from app.config import config


async def create_database_if_not_exists():
    """Create the database if it doesn't exist"""
    # Use individual config values for connection
    db_host = config.DB_HOST
    db_port = config.DB_PORT
    db_user = config.DB_USER
    db_password = config.DB_PASSWORD
    db_name = config.DB_NAME
    
    # Connection string for admin connection (to default postgres database)
    admin_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
    
    try:
        # Connect to default postgres database first
        conn = await asyncpg.connect(admin_url)
        
        # Check if our database exists
        exists = await conn.fetchval(
            f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"
        )
        
        if not exists:
            logger.info(f"Database '{db_name}' does not exist. Creating it...")
            await conn.execute(f"CREATE DATABASE {db_name}")
            logger.info(f"Database '{db_name}' created successfully!")
        else:
            logger.info(f"Database '{db_name}' already exists.")
            
        await conn.close()
        
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise


async def create_tables():
    """Create all database tables and indexes"""
    try:
        engine = get_engine()
        logger.info("Creating database tables...")
        
        async with engine.begin() as conn:
            # Create all tables defined in models
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully!")
            
        await engine.dispose()
        logger.info("Database engine disposed.")
        
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise


async def main():
    """Main function to run database creation"""
    print("Starting database setup...")
    
    # Step 1: Create database if it doesn't exist
    await create_database_if_not_exists()
    
    # Step 2: Create tables
    await create_tables()
    
    print("Database setup completed!")


if __name__ == "__main__":
    asyncio.run(main())
