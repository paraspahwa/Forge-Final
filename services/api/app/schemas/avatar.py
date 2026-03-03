"""
Avatar schemas
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class AvatarBase(BaseModel):
    """Base avatar schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class AvatarCreate(AvatarBase):
    """Avatar creation schema"""
    character_type: str = Field(..., pattern="^(anime|realistic)$")
    expressions: Optional[List[str]] = Field(
        default=["happy", "sad", "angry", "surprised", "neutral"],
        description="List of expressions to generate"
    )
    appearance: Optional[Dict[str, Any]] = Field(default_factory=dict)
    seed: Optional[int] = Field(None, description="Random seed for reproducibility")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "My Anime Character",
            "description": "A blue-haired magical girl",
            "character_type": "anime",
            "appearance": {
                "hair_color": "blue",
                "eye_color": "green",
                "outfit": "school uniform"
            },
            "seed": 42
        }
    })


class AvatarUpdate(BaseModel):
    """Avatar update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_favorite: Optional[bool] = None
    status: Optional[str] = Field(None, pattern="^(active|archived)$")


class AvatarResponse(AvatarBase):
    """Avatar response schema"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    character_type: str
    slug: Optional[str] = None
    appearance: Dict[str, Any]
    expressions: Dict[str, str]  # emotion -> URL
    usage_count: int
    is_favorite: bool
    status: str
    created_at: str


class AvatarListResponse(BaseModel):
    """Avatar list response"""
    items: List[AvatarResponse]
    total: int
    page: int
    per_page: int