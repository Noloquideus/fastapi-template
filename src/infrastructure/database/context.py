from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.settings import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
    echo=False
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
