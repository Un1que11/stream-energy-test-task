from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from collections.abc import AsyncGenerator
from typing import Annotated

from app.config import settings
from app.models import *

async_engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=True,
    future=True
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None, None]:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]