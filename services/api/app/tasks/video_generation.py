# app/tasks/video_generation.py
"""
Celery tasks for video generation
"""

import os
from datetime import datetime

from celery import shared_task
from sqlalchemy import select
from asgiref.sync import async_to_sync  # Better than raw asyncio.run

from app.core.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.core.logging import get_logger
from app.core.storage import storage_service
from app.models.video import Video, VideoStatus
from app.models.avatar import Avatar
from app.services.video_generation import video_generation_service
from app.services.voice import voice_service
from app.services.story_parser import story_parser_service

logger = get_logger(__name__)


@celery_app.task(bind=True, max_retries=3)
def generate_video_task(self, video_id: str, user_id: str):
    """
    Celery task for video generation
    """
    # Use async_to_sync to run async code in sync Celery context
    return async_to_sync(_generate_video_async)(self, video_id, user_id)


async def _generate_video_async(self, video_id: str, user_id: str):
    """
    Async implementation of video generation
    """
    async with AsyncSessionLocal() as db:
        try:
            # Fetch video
            result = await db.execute(
                select(Video).where(Video.id == video_id, Video.user_id == user_id)
            )
            video = result.scalar_one_or_none()
            
            if not video:
                logger.error(f"Video {video_id} not found")
                return {"status": "error", "message": "Video not found"}
            
            # Update status to processing
            video.status = VideoStatus.GENERATING_VIDEO
            video.current_task = "Initializing generation pipeline"
            await db.commit()
            
            logger.info(f"Starting video generation for {video_id}")
            
            # TODO: Implement your actual generation logic here
            # Example steps:
            # 1. Parse story
            # 2. Generate images for scenes
            # 3. Generate audio/narration
            # 4. Assemble video
            # 5. Upload to storage
            
            # Update video on success
            video.status = VideoStatus.COMPLETED
            video.completed_at = datetime.utcnow()
            video.video_url = f"https://storage.animeforge.ai/videos/{video_id}.mp4"
            await db.commit()
            
            logger.info(f"Video generation completed for {video_id}")
            return {"status": "success", "video_id": str(video_id)}
            
        except Exception as exc:
            await db.rollback()
            logger.error(f"Video generation failed for {video_id}: {exc}")
            
            # Update status to failed
            video.status = VideoStatus.FAILED
            video.error_message = str(exc)
            await db.commit()
            
            # Retry logic
            if self.request.retries < self.max_retries:
                logger.info(f"Retrying video generation for {video_id}, attempt {self.request.retries + 1}")
                raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))
            
            return {"status": "error", "message": str(exc)}