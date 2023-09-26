from sqlalchemy.ext.asyncio import (AsyncSession,
                                    async_sessionmaker,
                                    create_async_engine)

from app.core.config import settings

engine = create_async_engine(settings.db_url,
                             echo=True, future=True)


async def get_session() -> AsyncSession:
    try:
        async_session = async_sessionmaker(
            bind=engine, expire_on_commit=False
        )

        async with async_session() as session:
            yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
