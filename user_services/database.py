from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "postgresql+asyncpg://devops:devops24@localhost:5432/user_service"

#engine is the actual conn to the db
engine = create_async_engine(DATABASE_URL, echo=True) 
#db session for handling queries
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
