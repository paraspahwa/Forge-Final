"""
User management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_db
from app.core.logging import get_logger
from app.models.user import User
from app.schemas.auth import UserResponse
from app.api.v1.endpoints.auth import get_current_active_user, get_current_user

logger = get_logger(__name__)
router = APIRouter()


@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
):
    """Get user statistics"""
    return {
        "videos_generated_this_month": current_user.videos_generated_this_month,
        "videos_limit": current_user.videos_limit,
        "remaining_videos": current_user.get_remaining_videos(),
        "tier": current_user.tier.value,
        "subscription_status": current_user.subscription_status,
        "country": current_user.country_code,
    }


@router.get("/preferences")
async def get_preferences(
    current_user: User = Depends(get_current_active_user),
):
    """Get user preferences"""
    return {
        "preferred_character_type": current_user.preferred_character_type,
        "preferred_voice_gender": current_user.preferred_voice_gender,
        "timezone": current_user.timezone,
    }


@router.put("/preferences")
async def update_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user preferences"""
    allowed = [
        "preferred_character_type",
        "preferred_voice_gender",
        "timezone",
    ]
    
    for key in allowed:
        if key in preferences:
            setattr(current_user, key, preferences[key])
    
    await db.commit()
    
    return {"message": "Preferences updated", "preferences": preferences}