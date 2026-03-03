"""
Video generation endpoints
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.logging import get_logger
from app.models.video import Video, VideoStatus
from app.models.avatar import Avatar
from app.models.user import User
from app.schemas.video import (
    VideoCreate,
    VideoUpdate,
    VideoResponse,
    VideoListResponse,
    VideoStatusResponse,
    StoryParseRequest,
    StoryParseResponse,
    Scene,
)
from app.api.v1.endpoints.auth import get_current_active_user
from app.services.video_generation import video_queue_service
from app.services.story_parser import story_parser_service

logger = get_logger(__name__)
router = APIRouter()


@router.post("/parse-story", response_model=StoryParseResponse)
async def parse_story(
    request: StoryParseRequest,
    current_user: User = Depends(get_current_active_user),
):
    """
    Parse story text into scenes using AI
    
    - Returns structured scenes with emotions and timing
    - Estimates total duration
    """
    try:
        scenes = await story_parser_service.parse_story(
            story_text=request.story_text,
            character_type=request.character_type,
            num_scenes=request.num_scenes,
        )
        
        # Calculate estimated duration
        total_duration = sum(scene.duration for scene in scenes)
        
        # Generate suggested title
        suggested_title = await story_parser_service.generate_title(
            story_text=request.story_text
        )
        
        return {
            "scenes": [scene.model_dump() for scene in scenes],
            "estimated_duration": total_duration,
            "suggested_title": suggested_title,
        }
        
    except Exception as e:
        logger.error(f"Story parsing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse story: {str(e)}",
        )


@router.post("/generate", response_model=VideoResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_video(
    video_data: VideoCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new video (async generation)
    
    - Validates user limits
    - Queues video generation task
    - Returns immediately with pending status
    """
    # Check if user can generate video
    if not current_user.can_generate_video(video_data.character_type):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Monthly video limit reached ({current_user.videos_limit}). Upgrade your plan.",
        )
    
    # Validate avatar exists and belongs to user
    result = await db.execute(
        select(Avatar).where(
            Avatar.id == video_data.avatar_id,
            Avatar.user_id == current_user.id
        )
    )
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    # Validate character type matches avatar
    if avatar.character_type.value != video_data.character_type:
        raise HTTPException(
            status_code=400,
            detail=f"Avatar is {avatar.character_type.value}, but video requests {video_data.character_type}",
        )
    
    # Create video record
    video = Video(
        user_id=current_user.id,
        avatar_id=avatar.id,
        title=video_data.title,
        description=video_data.description,
        character_type=video_data.character_type,
        story_text=video_data.story_text,
        config={
            "voice_gender": video_data.voice_gender,
            "video_quality": video_data.video_quality,
            "add_background_music": video_data.add_background_music,
        },
        status=VideoStatus.PENDING,
        progress=0,
    )
    
    db.add(video)
    await db.commit()
    await db.refresh(video)
    
    # Queue video generation task
    try:
        task_id = await video_queue_service.queue_video_generation(
            video_id=str(video.id),
            user_id=str(current_user.id),
        )
        video.celery_task_id = task_id
        await db.commit()
        
        logger.info(f"Video queued: {video.id} (task: {task_id})")
        
    except Exception as e:
        logger.error(f"Failed to queue video: {e}")
        video.status = VideoStatus.FAILED
        video.error_message = f"Failed to queue: {str(e)}"
        await db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start video generation",
        )
    
    # Increment user's video count
    current_user.videos_generated_this_month += 1
    if video_data.character_type == "anime":
        current_user.anime_videos_this_month += 1
    else:
        current_user.realistic_videos_this_month += 1
    
    await db.commit()
    
    return video.to_dict()


@router.get("/", response_model=VideoListResponse)
async def list_videos(
    status: Optional[str] = Query(None, regex="^(pending|processing|completed|failed)$"),
    character_type: Optional[str] = Query(None, regex="^(anime|realistic)$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List user's videos with filtering"""
    query = select(Video).where(Video.user_id == current_user.id)
    
    # Map status filter
    if status:
        status_map = {
            "pending": [VideoStatus.PENDING, VideoStatus.QUEUED],
            "processing": [
                VideoStatus.PARSING_STORY,
                VideoStatus.GENERATING_IMAGES,
                VideoStatus.GENERATING_AUDIO,
                VideoStatus.GENERATING_VIDEO,
                VideoStatus.ASSEMBLING,
            ],
            "completed": [VideoStatus.COMPLETED],
            "failed": [VideoStatus.FAILED, VideoStatus.CANCELLED],
        }
        query = query.where(Video.status.in_(status_map[status]))
    
    if character_type:
        query = query.where(Video.character_type == character_type)
    
    # Order by newest first
    query = query.order_by(Video.created_at.desc())
    
    # Count total
    count_result = await db.execute(
        select(func.count(Video.id)).where(Video.user_id == current_user.id)
    )
    total = count_result.scalar()
    
    # Paginate
    query = query.offset((page - 1) * per_page).limit(per_page)
    
    result = await db.execute(query)
    videos = result.scalars().all()
    
    return {
        "items": [video.to_dict() for video in videos],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get video details"""
    result = await db.execute(
        select(Video).where(
            Video.id == str(video_id),
            Video.user_id == current_user.id
        )
    )
    video = result.scalar_one_or_none()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return video.to_dict()


@router.get("/{video_id}/status", response_model=VideoStatusResponse)
async def get_video_status(
    video_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get real-time video generation status"""
    result = await db.execute(
        select(Video).where(
            Video.id == str(video_id),
            Video.user_id == current_user.id
        )
    )
    video = result.scalar_one_or_none()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Calculate estimated time remaining (rough estimate)
    estimated_time = None
    if video.status in [VideoStatus.GENERATING_IMAGES, VideoStatus.GENERATING_VIDEO]:
        # Rough estimate: 30 seconds per remaining scene
        remaining_scenes = len(video.scenes) - (video.progress // (100 // max(len(video.scenes), 1)))
        estimated_time = remaining_scenes * 30
    
    return {
        "id": str(video.id),
        "status": video.status.value,
        "progress": video.progress,
        "current_task": video.current_task,
        "task_message": video.task_message,
        "video_url": video.video_url,
        "estimated_time_remaining": estimated_time,
    }


@router.delete("/{video_id}")
async def delete_video(
    video_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a video and its assets"""
    result = await db.execute(
        select(Video).where(
            Video.id == str(video_id),
            Video.user_id == current_user.id
        )
    )
    video = result.scalar_one_or_none()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # TODO: Delete files from storage
    # await storage_service.delete_file(video.video_url)
    
    await db.delete(video)
    await db.commit()
    
    return {"message": "Video deleted successfully"}


@router.post("/{video_id}/retry")
async def retry_video(
    video_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Retry failed video generation"""
    result = await db.execute(
        select(Video).where(
            Video.id == str(video_id),
            Video.user_id == current_user.id
        )
    )
    video = result.scalar_one_or_none()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if video.status != VideoStatus.FAILED:
        raise HTTPException(status_code=400, detail="Only failed videos can be retried")
    
    if video.retry_count >= video.max_retries:
        raise HTTPException(status_code=400, detail="Maximum retry attempts reached")
    
    # Reset status and queue again
    video.status = VideoStatus.PENDING
    video.retry_count += 1
    video.error_message = None
    await db.commit()
    
    # Re-queue
    task_id = await video_queue_service.queue_video_generation(
        video_id=str(video.id),
        user_id=str(current_user.id),
    )
    video.celery_task_id = task_id
    await db.commit()
    
    return {"message": "Video queued for retry", "task_id": task_id}