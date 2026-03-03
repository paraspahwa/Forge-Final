"""
Video model for generated content
"""

import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class VideoStatus(str, PyEnum):
    """Video generation status"""
    PENDING = "pending"
    QUEUED = "queued"
    PARSING_STORY = "parsing_story"
    GENERATING_IMAGES = "generating_images"
    GENERATING_AUDIO = "generating_audio"
    GENERATING_VIDEO = "generating_video"
    ASSEMBLING = "assembling"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Video(Base):
    """Video model"""
    __tablename__ = "videos"
    __table_args__ = (
        {"postgresql_indexes": [
            {"name": "idx_video_user_status", "columns": ["user_id", "status"]},
            {"name": "idx_video_created", "columns": ["created_at"]},
        ]}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    avatar_id = Column(UUID(as_uuid=True), ForeignKey("avatars.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Video info
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    slug = Column(String(100), nullable=True, unique=True)
    
    # Character type used
    character_type = Column(String(20), nullable=False)  # anime or realistic
    
    # Source content
    story_text = Column(Text, nullable=True)
    story_prompt = Column(Text, nullable=True)  # AI-generated or user prompt
    scenes = Column(JSON, default=list)  # Parsed scenes array
    
    # Generation configuration
    config = Column(JSON, default=dict)
    # {
    #   "voice_gender": "female",
    #   "voice_speed": 1.0,
    #   "background_music": false,
    #   "video_quality": "1080p",
    #   "effects": ["zoom_in", "pan_left"]
    # }
    
    # Generation status
    status = Column(Enum(VideoStatus), default=VideoStatus.PENDING, index=True)
    progress = Column(Integer, default=0)  # 0-100
    
    # Current task info
    current_task = Column(String(100), nullable=True)  # e.g., "generating_scene_3"
    task_message = Column(Text, nullable=True)  # User-friendly status message
    
    # Output files
    video_url = Column(String(500), nullable=True)
    video_duration = Column(Integer, default=0)  # seconds
    video_size = Column(Integer, default=0)  # bytes
    video_format = Column(String(10), default="mp4")
    video_quality = Column(String(10), default="1080p")
    
    thumbnail_url = Column(String(500), nullable=True)
    
    # Audio
    audio_url = Column(String(500), nullable=True)
    voice_used = Column(String(50), nullable=True)  # e.g., "en-US-AriaNeural"
    
    # Scene assets (intermediate files)
    scene_assets = Column(JSON, default=list)  # Array of scene file URLs
    
    # Social media
    posted_to = Column(JSON, default=list)  # ["tiktok", "youtube"]
    scheduled_post = Column(DateTime, nullable=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    error_code = Column(String(50), nullable=True)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    # Celery task ID
    celery_task_id = Column(String(100), nullable=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)  # When generation started
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="videos")
    avatar = relationship("Avatar", back_populates="videos")
    
    def __repr__(self):
        return f"<Video {self.title} ({self.status.value}, {self.user_id})>"
    
    def to_dict(self, include_assets=False):
        """Convert to dictionary"""
        data = {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "character_type": self.character_type,
            "status": self.status.value,
            "progress": self.progress,
            "current_task": self.current_task,
            "task_message": self.task_message,
            "video_url": self.video_url,
            "video_duration": self.video_duration,
            "thumbnail_url": self.thumbnail_url,
            "scenes_count": len(self.scenes) if self.scenes else 0,
            "posted_to": self.posted_to,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
        
        if self.avatar:
            data["avatar"] = {
                "id": str(self.avatar.id),
                "name": self.avatar.name,
                "character_type": self.avatar.character_type.value,
            }
        
        if include_assets and self.scenes:
            data["scenes"] = self.scenes
        
        return data
    
    def get_duration_formatted(self) -> str:
        """Get duration in MM:SS format"""
        minutes = self.video_duration // 60
        seconds = self.video_duration % 60
        return f"{minutes}:{seconds:02d}"