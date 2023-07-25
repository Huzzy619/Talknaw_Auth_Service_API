from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.config import settings
from sqlalchemy.orm import DeclarativeBase

async_engine = create_async_engine(settings.database_url.__str__(), echo=settings.db_echo, future=True)


async def db_session() -> AsyncSession:
    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session



class Base(AsyncAttrs, DeclarativeBase):
    pass

# Base = declarative_base()


AnSession = Annotated[AsyncSession,  Depends(db_session)]

