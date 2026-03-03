"""
AnimeForge Duo - FastAPI Backend
Dual Character (Anime + Realistic) Video Generation Platform
"""

import os
import sys
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import engine, Base
from app.core.logging import get_logger

logger = get_logger(__name__)

# Initialize Sentry
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        environment=settings.ENVIRONMENT,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info(f"Starting AnimeForge API in {settings.ENVIRONMENT} mode")
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables verified")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AnimeForge API")
    await engine.dispose()


app = FastAPI(
    title="AnimeForge Duo API",
    description="""
    AI Video Generation Platform supporting both Anime and Realistic characters.
    
    Features:
    - Dual character generation (Anime + Realistic)
    - Automated video creation with voice
    - Country-based PPP pricing
    - Social media auto-posting
    """,
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

# Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    from uuid import uuid4
    request.state.request_id = str(uuid4())[:8]
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
    }


@app.get("/health/detailed", tags=["Health"])
async def health_detailed():
    """Detailed health check with dependencies"""
    checks = {
        "api": "healthy",
        "database": "unknown",
        "redis": "unknown",
    }
    
    # Check database
    try:
        from sqlalchemy import text
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
    
    # Check Redis
    try:
        import redis.asyncio as redis
        r = redis.from_url(settings.REDIS_URL)
        await r.ping()
        checks["redis"] = "healthy"
        await r.close()
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"
    
    all_healthy = all(c == "healthy" for c in checks.values() if c != "unknown")
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "checks": checks,
    }


@app.get("/", tags=["Root"])
async def root():
    """API root"""
    return {
        "name": "AnimeForge Duo API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health",
    }