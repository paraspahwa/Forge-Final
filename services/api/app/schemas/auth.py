"""
Authentication schemas
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User registration schema"""
    password: str = Field(..., min_length=8, max_length=100)
    country_code: Optional[str] = None  # Auto-detected if not provided
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "user@example.com",
            "password": "securepassword123",
            "full_name": "John Doe",
        }
    })


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "user@example.com",
            "password": "securepassword123",
        }
    })


class UserResponse(UserBase):
    """User response schema"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    country_code: str
    tier: str
    subscription_status: str
    videos_generated_this_month: int
    videos_limit: int
    preferred_character_type: str
    is_verified: bool
    created_at: Optional[str] = None
    last_login: Optional[str] = None


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "token_type": "bearer",
            "user": {
                "id": "uuid",
                "email": "user@example.com",
                "tier": "free",
            }
        }
    })


class TokenRefresh(BaseModel):
    """Token refresh schema"""
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Password reset request schema"""
    email: EmailStr


class PasswordReset(BaseModel):
    """Password reset schema"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)