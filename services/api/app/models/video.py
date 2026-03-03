"""
Video model for generated content
"""

import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    JSON, 
    Column, 
    DateTime, 
    Enum, 
    ForeignKey, 
    Integer, 
    String, 
    Text, 
    Index,
)
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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    avatar_id = Column(UUID(as_uuid=True), ForeignKey("avatars.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Video info
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    slug = Column(String(100), nullable=True, unique=True)
    
    # Character type used
    character_type = Column(String(20), nullable=False)
    
    # Source content
    story_text = Column(Text, nullable=True)
    story_prompt = Column(Text, nullable=True)
    scenes = Column(JSON, default=list)
    
    # Generation configuration
    config = Column(JSON, default=dict)
    
    # Generation status
    status = Column(Enum(VideoStatus), default=VideoStatus.PENDING, index=True)
    progress = Column(Integer, default=0)
    
    # Current task info
    current_task = Column(String(100), nullable=True)
    task_message = Column(Text, nullable=True)
    
    # Output files
    video_url = Column(String(500), nullable=True)
    video_duration = Column(Integer, default=0)
    video_size = Column(Integer, default=0)
    video_format = Column(String(10), default="mp4")
    video_quality = Column(String(10), default="1080p")
    
    thumbnail_url = Column(String(500), nullable=True)
    
    # Audio
    audio_url = Column(String(500), nullable=True)
    voice_used = Column(String(50), nullable=True)
    
    # Scene assets
    scene_assets = Column(JSON, default=list)
    
    # Social media
    posted_to = Column(JSON, default=list)
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
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="videos")
    avatar = relationship("Avatar", back_populates="videos")
    
    # Table indexes
    __table_args__ = (
        Index('idx_video_user_status', 'user_id', 'status'),
        Index('idx_video_created', 'created_at'),
    )
    
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