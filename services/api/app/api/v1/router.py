"""
API v1 router
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, avatars, videos, payments, users, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(avatars.router, prefix="/avatars", tags=["Avatars"])
api_router.include_router(videos.router, prefix="/videos", tags=["Videos"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])