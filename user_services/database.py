import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger("UserService")

DB_USER = os.getenv("POSTGRES_USER", "devops")  
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "devops24")
DB_HOST = os.getenv("POSTGRES_HOST", "postgresql") 
DB_NAME = os.getenv("POSTGRES_DB", "user_service")  

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/user_service"

# Engine is the actual connection to the DB
engine = create_async_engine(DATABASE_URL, echo=True) 
# DB session for handling queries
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        logger.info("Database connection successful")
        yield session
