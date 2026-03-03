"""
Celery configuration for background tasks
"""

from celery import Celery
from celery.signals import task_prerun, task_postrun

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Create Celery app
celery_app = Celery(
    "animeforge",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.video_generation",
        "app.tasks.social_posting",
        "app.tasks.notifications",
    ],
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,  # 10 minutes max
    task_soft_time_limit=540,  # 9 minutes soft limit
    worker_prefetch_multiplier=1,  # Don't prefetch tasks
    worker_max_tasks_per_child=50,  # Restart worker after 50 tasks
)


@task_prerun.connect
def task_prerun_handler(task_id, task, args, kwargs, **extras):
    """Log task start"""
    logger.info(f"Task {task.name}[{task_id}] started")


@task_postrun.connect
def task_postrun_handler(task_id, task, args, kwargs, retval, state, **extras):
    """Log task completion"""
    logger.info(f"Task {task.name}[{task_id}] finished with state: {state}")


# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "reset-monthly-quotas": {
        "task": "app.tasks.notifications.reset_monthly_quotas",
        "schedule": "0 0 1 * *",  # First day of month at midnight
    },
    "cleanup-old-videos": {
        "task": "app.tasks.notifications.cleanup_old_videos",
        "schedule": 86400.0,  # Daily
    },
}