"""
Database configuration with SQLAlchemy async
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Create async engine
if settings.ENVIRONMENT == "testing":
    engine = create_async_engine(
        settings.DATABASE_URL,
        future=True,
        poolclass=NullPool,
    )
else:
    engine = create_async_engine(
        settings.DATABASE_URL,
        future=True,
        echo=settings.DEBUG,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
    )

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Dependency for getting database session.
    Use as: db: AsyncSession = Depends(get_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")


async def close_db():
    """Close database connections"""
    await engine.dispose()
    logger.info("Database connections closed")