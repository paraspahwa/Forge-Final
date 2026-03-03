"""
Video schemas
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class Scene(BaseModel):
    """Video scene schema"""
    scene_number: int
    description: str
    dialogue: Optional[str] = None
    emotion: str = "neutral"
    duration: int = Field(default=5, ge=1, le=60)
    background_prompt: Optional[str] = None


class VideoBase(BaseModel):
    """Base video schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class VideoCreate(VideoBase):
    """Video creation schema"""
    avatar_id: str
    character_type: str = Field(..., pattern="^(anime|realistic)$")
    story_text: str = Field(..., min_length=10, max_length=10000)
    
    # Generation options
    voice_gender: str = Field(default="female", pattern="^(male|female)$")
    video_quality: str = Field(default="1080p", pattern="^(720p|1080p|4k)$")
    add_background_music: bool = False
    auto_post_to: Optional[List[str]] = Field(default_factory=list)
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "My First Video",
            "avatar_id": "uuid-here",
            "character_type": "anime",
            "story_text": "Once upon a time...",
            "voice_gender": "female",
        }
    })


class VideoUpdate(BaseModel):
    """Video update schema (for metadata only)"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class VideoResponse(VideoBase):
    """Video response schema"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    character_type: str
    status: str
    progress: int
    current_task: Optional[str] = None
    task_message: Optional[str] = None
    video_url: Optional[str] = None
    video_duration: int
    thumbnail_url: Optional[str] = None
    scenes_count: int
    posted_to: List[str]
    avatar: Optional[Dict[str, Any]] = None
    created_at: str
    completed_at: Optional[str] = None


class VideoStatusResponse(BaseModel):
    """Video status check response"""
    id: str
    status: str
    progress: int
    current_task: Optional[str]
    task_message: Optional[str]
    video_url: Optional[str]
    estimated_time_remaining: Optional[int] = None  # seconds


class VideoListResponse(BaseModel):
    """Video list response"""
    items: List[VideoResponse]
    total: int
    page: int
    per_page: int


class StoryParseRequest(BaseModel):
    """Story parsing request"""
    story_text: str = Field(..., min_length=10, max_length=10000)
    character_type: str = Field(..., pattern="^(anime|realistic)$")
    num_scenes: int = Field(default=5, ge=1, le=20)


class StoryParseResponse(BaseModel):
    """Story parsing response"""
    scenes: List[Scene]
    estimated_duration: int  # seconds
    suggested_title: Optional[str] = None