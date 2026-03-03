"""
Application configuration with environment variables
"""

from typing import List, Optional
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    # App
    APP_NAME: str = "AnimeForge Duo"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-in-production"
    
    # URLs
    FRONTEND_URL: str = "http://localhost:3000"
    MOBILE_URL: str = "exp://localhost:8081"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/animeforge"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://localhost:3000",
        "http://localhost:8081",
        "https://animeforge.vercel.app",
        "https://animeforge.app",
        "https://www.animeforge.app",
    ]
    
    # AI Services
    SEGMIND_API_KEY: str = ""
    LEPTON_API_KEY: str = ""
    RUNPOD_API_KEY: str = ""
    RUNPOD_SADTALKER_ENDPOINT: str = ""
    
    # Storage (Cloudflare R2 / AWS S3 compatible)
    R2_ENDPOINT_URL: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = "animeforge"
    R2_PUBLIC_URL: str = ""
    R2_REGION: str = "auto"
    
    # Payments (Razorpay)
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    RAZORPAY_WEBHOOK_SECRET: str = ""
    
    # GeoIP
    MAXMIND_LICENSE_KEY: str = ""
    MAXMIND_DB_PATH: str = "./GeoLite2-Country.mmdb"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    
    # Video Generation
    DEFAULT_VIDEO_DURATION: int = 30
    MAX_VIDEO_DURATION: int = 300  # 5 minutes
    MAX_SCENES_PER_VIDEO: int = 20
    MAX_CHARACTERS_PER_USER: int = 10
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()