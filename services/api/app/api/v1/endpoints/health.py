"""
Health check endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db, engine
from app.core.config import settings

router = APIRouter()


@router.get("/")
async def basic_health():
    """Basic health check - always returns 200 if server is up"""
    return {
        "status": "healthy",
        "service": "animeforge-api",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }


@router.get("/detailed")
async def detailed_health(db: AsyncSession = Depends(get_db)):
    """Detailed health check with dependency status"""
    checks = {
        "api": {"status": "healthy", "response_time_ms": 0},
        "database": {"status": "unknown", "response_time_ms": 0},
        "storage": {"status": "unknown", "response_time_ms": 0},
    }
    
    import time
    
    # Check database
    start = time.time()
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = {
            "status": "healthy",
            "response_time_ms": round((time.time() - start) * 1000, 2),
        }
    except Exception as e:
        checks["database"] = {
            "status": "unhealthy",
            "error": str(e),
            "response_time_ms": round((time.time() - start) * 1000, 2),
        }
    
    # Check storage (R2/S3)
    start = time.time()
    try:
        from app.core.storage import storage_service
        # Try to list buckets or perform a simple operation
        storage_service.client.list_buckets()
        checks["storage"] = {
            "status": "healthy",
            "response_time_ms": round((time.time() - start) * 1000, 2),
        }
    except Exception as e:
        checks["storage"] = {
            "status": "unhealthy" if "InvalidAccessKeyId" in str(e) else "degraded",
            "error": str(e),
            "response_time_ms": round((time.time() - start) * 1000, 2),
        }
    
    # Determine overall status
    all_healthy = all(c["status"] == "healthy" for c in checks.values())
    any_unhealthy = any(c["status"] == "unhealthy" for c in checks.values())
    
    if all_healthy:
        overall_status = "healthy"
    elif any_unhealthy:
        overall_status = "unhealthy"
    else:
        overall_status = "degraded"
    
    return {
        "status": overall_status,
        "checks": checks,
        "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
    }


@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """
    Kubernetes-style readiness probe
    
    Returns 200 only when ready to serve traffic
    """
    try:
        await db.execute(text("SELECT 1"))
        return {"ready": True}
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Not ready")


@router.get("/live")
async def liveness_check():
    """
    Kubernetes-style liveness probe
    
    Returns 200 if server is running (even if not fully ready)
    """
    return {"alive": True}