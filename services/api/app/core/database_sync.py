"""
Sync database configuration for Celery tasks
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Convert async URL to sync URL
def get_sync_url():
    url = settings.DATABASE_URL
    if "asyncpg" in url:
        return url.replace("postgresql+asyncpg", "postgresql+psycopg2")
    return url

engine = create_engine(
    get_sync_url(),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_sync_db():
    """Sync database session for Celery tasks"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()