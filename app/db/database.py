from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.main import settings

DATABASE_URL = settings.database_url

engine = AsyncEngine(DATABASE_URL, echo=True, future=True)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(
        bind=engine, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
