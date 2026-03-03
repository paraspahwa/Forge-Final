"""
Celery tasks for video generation
"""

import os
from datetime import datetime

from celery import shared_task
from sqlalchemy import select

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
    
    This runs asynchronously in a worker process
    """
    import asyncio
    
    # Run async function in sync context
    asyncio.run(_generate_video_async(self, video_id, user_id))


async def _generate_video_async(task, video_id: str, user_id: str):
    """Async video generation logic"""
    
    async with AsyncSessionLocal() as db:
        try:
            # Get video record
            result = await db.execute(select(Video).where(Video.id == video_id))
            video = result.scalar_one_or_none()
            
            if not video:
                logger.error(f"Video not found: {video_id}")
                return
            
            # Update status
            video.status = VideoStatus.PARSING_STORY
            video.started_at = datetime.utcnow()
            video.progress = 10
            await db.commit()
            
            # Parse story if needed
            if not video.scenes:
                video.status = VideoStatus.PARSING_STORY
                video.task_message = "Parsing story into scenes..."
                await db.commit()
                
                scenes = await story_parser_service.parse_story(
                    story_text=video.story_text,
                    character_type=video.character_type,
                )
                video.scenes = [s.model_dump() for s in scenes]
                video.progress = 20
                await db.commit()
            
            # Get avatar
            result = await db.execute(select(Avatar).where(Avatar.id == video.avatar_id))
            avatar = result.scalar_one_or_none()
            
            if not avatar:
                raise Exception("Avatar not found")
            
            # Generate audio for each scene
            video.status = VideoStatus.GENERATING_AUDIO
            video.task_message = "Generating voice audio..."
            video.progress = 30
            await db.commit()
            
            audio_paths = []
            for i, scene in enumerate(video.scenes):
                if scene.get("dialogue"):
                    audio_path = await voice_service.generate(
                        text=scene["dialogue"],
                        character_type=video.character_type,
                        gender=video.config.get("voice_gender", "female"),
                        output_path=f"/tmp/video_{video_id}_scene_{i}.mp3",
                    )
                    audio_paths.append(audio_path)
                else:
                    audio_paths.append(None)
            
            video.progress = 50
            await db.commit()
            
            # Generate video based on type
            output_path = f"/tmp/video_{video_id}_final.mp4"
            
            if video.character_type == "anime":
                video.status = VideoStatus.GENERATING_VIDEO
                video.task_message = "Generating anime video..."
                video.progress = 60
                await db.commit()
                
                await video_generation_service.generate_anime_video(
                    scenes=video.scenes,
                    expression_images=avatar.expressions,
                    audio_paths=audio_paths,
                    output_path=output_path,
                )
                
            else:  # realistic
                video.status = VideoStatus.GENERATING_VIDEO
                video.task_message = "Generating realistic talking head..."
                video.progress = 60
                await db.commit()
                
                # For realistic, use first scene's audio or combine all
                main_audio = audio_paths[0] if audio_paths else None
                
                await video_generation_service.generate_realistic_video(
                    face_image_url=avatar.expressions.get("neutral"),
                    audio_path=main_audio,
                    output_path=output_path,
                )
            
            video.progress = 90
            video.task_message = "Uploading video..."
            await db.commit()
            
            # Upload to storage
            video_url = await storage_service.upload_file(
                file_path=output_path,
                destination_path=f"videos/{user_id}/{video_id}/video.mp4",
                content_type="video/mp4",
            )
            
            video.video_url = video_url
            video.status = VideoStatus.COMPLETED
            video.progress = 100
            video.task_message = "Video completed!"
            video.completed_at = datetime.utcnow()
            
            # Get video duration
            # TODO: Use ffprobe to get actual duration
            
            await db.commit()
            
            logger.info(f"Video generation completed: {video_id}")
            
            # Cleanup temp files
            try:
                os.remove(output_path)
                for path in audio_paths:
                    if path and os.path.exists(path):
                        os.remove(path)
            except Exception as e:
                logger.warning(f"Cleanup failed: {e}")
            
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            
            video.status = VideoStatus.FAILED
            video.error_message = str(e)
            video.retry_count += 1
            await db.commit()
            
            # Retry if attempts remaining
            if video.retry_count < video.max_retries:
                raise self.retry(exc=e, countdown=60)
            
            raise