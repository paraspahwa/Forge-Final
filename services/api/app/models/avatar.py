"""
Avatar model for both Anime and Realistic characters
"""

import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class CharacterType(str, PyEnum):
    """Character type enum"""
    ANIME = "anime"
    REALISTIC = "realistic"


class Avatar(Base):
    """Avatar model"""
    __tablename__ = "avatars"
    __table_args__ = (
        # Index for faster queries by user and type
        {"postgresql_indexes": [
            {"name": "idx_avatar_user_type", "columns": ["user_id", "character_type"]},
        ]}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Character type
    character_type = Column(Enum(CharacterType), nullable=False, index=True)
    
    # Basic info
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    slug = Column(String(100), nullable=True, unique=True)
    
    # Appearance details (flexible JSON)
    appearance = Column(JSON, default=dict)
    # Example: {
    #   "hair_color": "blue",
    #   "hair_style": "long",
    #   "eye_color": "green",
    #   "outfit": "school uniform",
    #   "age_appearance": "teen",
    #   "ethnicity": "asian",  # for realistic
    #   "style": "chibi",  # for anime
    # }
    
    # Expression images (URLs)
    expressions = Column(JSON, default=dict, nullable=False)
    # {
    #   "happy": "https://.../happy.png",
    #   "sad": "https://.../sad.png",
    #   "angry": "https://.../angry.png",
    #   "surprised": "https://.../surprised.png",
    #   "neutral": "https://.../neutral.png"
    # }
    
    # Generation metadata
    generation_prompt = Column(Text, nullable=True)
    generation_negative_prompt = Column(Text, nullable=True)
    generation_seed = Column(Integer, nullable=True)
    generation_model = Column(String(50), default="segmind")
    
    # Stats
    usage_count = Column(Integer, default=0)  # How many videos used this avatar
    is_favorite = Column(Boolean, default=False)
    
    # Status
    status = Column(String(20), default="active")  # active, archived, deleted
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="avatars")
    videos = relationship("Video", back_populates="avatar")
    
    def __repr__(self):
        return f"<Avatar {self.name} ({self.character_type.value}, {self.user_id})>"
    
    def to_dict(self, include_user=False):
        """Convert to dictionary"""
        data = {
            "id": str(self.id),
            "character_type": self.character_type.value,
            "name": self.name,
            "description": self.description,
            "slug": self.slug,
            "appearance": self.appearance,
            "expressions": self.expressions,
            "usage_count": self.usage_count,
            "is_favorite": self.is_favorite,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_user and self.user:
            data["user"] = self.user.to_dict()
        
        return data
    
    def get_expression_url(self, emotion: str) -> str:
        """Get expression URL by emotion"""
        emotion = emotion.lower()
        if emotion in self.expressions:
            return self.expressions[emotion]
        # Fallback to neutral
        return self.expressions.get("neutral", "")
    
    def get_all_expressions(self) -> list:
        """Get list of all available expressions"""
        return list(self.expressions.keys())