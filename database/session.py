from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from typing import Annotated
from fastapi import Depends
from ml_fastapi.config import settings


engine=create_async_engine(
    url=settings.postgres_url,
    echo=True,
)


async def create_db_table():
    async with engine.begin() as conn:
        from ml_fastapi.api.schemas.shipment import Shipment
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async_session_maker=sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        yield session


