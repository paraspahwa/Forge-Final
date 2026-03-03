"""
User model with country-based pricing support
"""

import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserTier(str, PyEnum):
    """User subscription tiers"""
    FREE = "free"
    STARTER = "starter"
    CREATOR = "creator"
    PRO = "pro"
    AGENCY = "agency"


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile
    full_name = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Country & Pricing (PPP)
    country_code = Column(String(2), default="US", index=True)
    detected_country = Column(String(2), nullable=True)
    detected_ip = Column(String(45), nullable=True)  # IPv6 max length
    
    # Subscription
    tier = Column(Enum(UserTier), default=UserTier.FREE, index=True)
    subscription_id = Column(String(255), nullable=True, index=True)
    subscription_status = Column(String(50), default="inactive")
    subscription_current_period_start = Column(DateTime, nullable=True)
    subscription_current_period_end = Column(DateTime, nullable=True)
    subscription_cancel_at_period_end = Column(Boolean, default=False)
    
    # Usage tracking (monthly reset)
    videos_generated_this_month = Column(Integer, default=0)
    anime_videos_this_month = Column(Integer, default=0)
    realistic_videos_this_month = Column(Integer, default=0)
    videos_limit = Column(Integer, default=4)  # 3 anime + 1 realistic for free
    
    # Preferences
    preferred_character_type = Column(String(20), default="anime")
    preferred_voice_gender = Column(String(10), default="female")
    timezone = Column(String(50), default="UTC")
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    last_active = Column(DateTime, nullable=True)
    
    # Relationships
    avatars = relationship(
        "Avatar",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    videos = relationship(
        "Video",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    subscriptions = relationship(
        "Subscription",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    
    def __repr__(self):
        return f"<User {self.email} ({self.country_code}, {self.tier.value})>"
    
    def to_dict(self, include_relations=False):
        """Convert to dictionary"""
        data = {
            "id": str(self.id),
            "email": self.email,
            "full_name": self.full_name,
            "avatar_url": self.avatar_url,
            "country_code": self.country_code,
            "tier": self.tier.value,
            "subscription_status": self.subscription_status,
            "videos_generated_this_month": self.videos_generated_this_month,
            "videos_limit": self.videos_limit,
            "preferred_character_type": self.preferred_character_type,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
        
        if include_relations:
            data["avatars"] = [a.to_dict() for a in self.avatars]
            data["videos"] = [v.to_dict() for v in self.videos[:10]]  # Last 10
        
        return data
    
    def can_generate_video(self, character_type: str = "anime") -> bool:
        """Check if user can generate another video this month"""
        if self.tier == UserTier.AGENCY:
            return True  # Unlimited
        
        total_used = self.videos_generated_this_month
        return total_used < self.videos_limit
    
    def get_remaining_videos(self) -> int:
        """Get remaining videos for this month"""
        if self.tier == UserTier.AGENCY:
            return 999999
        return max(0, self.videos_limit - self.videos_generated_this_month)