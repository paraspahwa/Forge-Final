"""
Periodic tasks and notifications
"""

from celery import shared_task
from sqlalchemy import select, func

from app.core.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.core.logging import get_logger
from app.models.user import User

logger = get_logger(__name__)


@celery_app.task
def reset_monthly_quotas():
    """Reset monthly video quotas for all users (run on 1st of month)"""
    import asyncio
    asyncio.run(_reset_quotas_async())


async def _reset_quotas_async():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()
        
        for user in users:
            user.videos_generated_this_month = 0
            user.anime_videos_this_month = 0
            user.realistic_videos_this_month = 0
        
        await db.commit()
        logger.info(f"Reset quotas for {len(users)} users")


@celery_app.task
def cleanup_old_videos():
    """Clean up old video files from storage"""
    # TODO: Implement cleanup logic
    logger.info("Running video cleanup")
    pass