"""
Celery tasks for social media posting
"""

from celery import shared_task

from app.core.celery_app import celery_app
from app.core.logging import get_logger

logger = get_logger(__name__)


@celery_app.task
def post_to_tiktok(video_url: str, caption: str, access_token: str):
    """Post video to TikTok"""
    # TODO: Implement TikTok API integration
    logger.info(f"Posting to TikTok: {video_url}")
    pass


@celery_app.task
def post_to_youtube(video_url: str, title: str, description: str, credentials: dict):
    """Post video to YouTube"""
    # TODO: Implement YouTube API integration
    logger.info(f"Posting to YouTube: {title}")
    pass