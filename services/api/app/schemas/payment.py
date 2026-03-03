"""
Payment schemas
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class PlanPrice(BaseModel):
    """Plan price schema"""
    usd: float
    local: Dict[str, Any]  # amount, currency, symbol


class PlanLimits(BaseModel):
    """Plan limits schema"""
    anime_videos: int
    realistic_videos: int
    features: list


class PlanResponse(BaseModel):
    """Plan response"""
    name: str
    price: PlanPrice
    limits: PlanLimits


class PlansListResponse(BaseModel):
    """Plans list response"""
    country: str
    currency: str
    plans: Dict[str, PlanResponse]


class SubscribeRequest(BaseModel):
    """Subscription request"""
    plan: str = Field(..., pattern="^(starter|creator|pro|agency)$")


class SubscribeResponse(BaseModel):
    """Subscription response"""
    subscription_id: str
    short_url: str
    amount: int
    currency: str
    key: str  # Razorpay key ID


class WebhookPayload(BaseModel):
    """Razorpay webhook payload (simplified)"""
    event: str
    payload: Dict[str, Any]