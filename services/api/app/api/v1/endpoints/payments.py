"""
Razorpay payment integration with PPP pricing
"""

import hmac
import hashlib
import json
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.logging import get_logger
from app.models.user import User, UserTier
from app.schemas.payment import (
    PlansListResponse,
    SubscribeRequest,
    SubscribeResponse,
    PlanResponse,
    PlanPrice,
    PlanLimits,
)
from app.services.pricing import get_localized_price, get_plan_limits, PLAN_CONFIGS
from app.api.v1.endpoints.auth import get_current_active_user

logger = get_logger(__name__)
router = APIRouter()


@router.get("/plans")
async def get_plans(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get available plans with PPP pricing for user's country
    
    Returns plans with prices in user's local currency
    """
    country = current_user.country_code or "US"
    
    plans = {}
    for plan_key in ["free", "starter", "creator", "pro", "agency"]:
        price = get_localized_price(country, plan_key)
        limits = get_plan_limits(plan_key)
        
        plans[plan_key] = {
            "name": plan_key.title(),
            "price": {
                "usd": price.display_price_usd,
                "local": {
                    "amount": price.local_amount,
                    "currency": price.local_currency,
                    "symbol": price.local_symbol,
                    "display": f"{price.local_symbol}{price.local_amount:,}",
                },
            },
            "limits": limits,
        }
    
    return {
        "country": country,
        "currency": price.local_currency,
        "plans": plans,
    }


@router.post("/subscribe")
async def create_subscription(
    request: SubscribeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create Razorpay subscription
    
    - Creates plan if not exists
    - Creates subscription with user metadata
    - Returns checkout URL
    """
    import razorpay
    
    if request.plan == "free":
        raise HTTPException(
            status_code=400,
            detail="Cannot subscribe to free plan. Choose starter, creator, pro, or agency.",
        )
    
    # Get localized price
    country = current_user.country_code or "US"
    price = get_localized_price(country, request.plan)
    
    # Initialize Razorpay
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create or get plan
    plan_id = f"animeforge_{request.plan}_{country}_{price.local_currency}".lower()
    
    try:
        # Try to fetch existing plan
        client.plan.fetch(plan_id)
        logger.info(f"Using existing plan: {plan_id}")
    except razorpay.errors.BadRequestError:
        # Create new plan
        logger.info(f"Creating new plan: {plan_id}")
        
        plan_data = {
            "period": "monthly",
            "interval": 1,
            "item": {
                "name": f"AnimeForge {request.plan.title()} - {country}",
                "amount": price.razorpay_amount,
                "currency": price.local_currency,
                "description": f"{request.plan.title()} plan for users in {country}",
            },
            "notes": {
                "country": country,
                "ppp_ratio": str(price.ppp_ratio),
            },
        }
        
        try:
            client.plan.create(plan_data)
        except Exception as e:
            logger.error(f"Failed to create plan: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to create subscription plan",
            )
    
    # Create subscription
    subscription_data = {
        "plan_id": plan_id,
        "total_count": 12,  # 1 year
        "quantity": 1,
        "customer_notify": 1,
        "notes": {
            "user_id": str(current_user.id),
            "email": current_user.email,
            "country": country,
            "plan": request.plan,
            "ppp_ratio": str(price.ppp_ratio),
        },
    }
    
    try:
        subscription = client.subscription.create(subscription_data)
        logger.info(f"Subscription created: {subscription['id']} for user {current_user.id}")
        
        return {
            "subscription_id": subscription["id"],
            "short_url": subscription.get("short_url", ""),
            "amount": price.local_amount,
            "currency": price.local_currency,
            "key": settings.RAZORPAY_KEY_ID,
        }
        
    except Exception as e:
        logger.error(f"Failed to create subscription: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create subscription",
        )


@router.post("/webhook")
async def razorpay_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Handle Razorpay webhooks
    
    Verifies signature and processes events:
    - subscription.charged: Activate user plan
    - subscription.cancelled: Downgrade to free
    - payment.failed: Log failure
    """
    # Get raw body
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")
    
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")
    
    # Verify webhook signature
    expected_signature = hmac.new(
        settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        logger.warning("Invalid webhook signature")
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Parse payload
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    event = payload.get("event")
    logger.info(f"Razorpay webhook received: {event}")
    
    # Handle events
    if event == "subscription.charged":
        await _handle_subscription_charged(payload, db)
    elif event == "subscription.cancelled":
        await _handle_subscription_cancelled(payload, db)
    elif event == "payment.failed":
        await _handle_payment_failed(payload, db)
    else:
        logger.info(f"Ignoring unhandled event: {event}")
    
    return {"status": "ok"}


async def _handle_subscription_charged(payload: dict, db: AsyncSession):
    """Handle successful subscription charge"""
    subscription = payload["payload"]["subscription"]["entity"]
    notes = subscription.get("notes", {})
    
    user_id = notes.get("user_id")
    plan = notes.get("plan")
    
    if not user_id or not plan:
        logger.error("Missing user_id or plan in subscription notes")
        return
    
    # Get user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        logger.error(f"User not found: {user_id}")
        return
    
    # Update user subscription
    try:
        user.tier = UserTier(plan)
        user.subscription_id = subscription["id"]
        user.subscription_status = "active"
        user.subscription_current_period_start = __import__("datetime").datetime.fromtimestamp(
            subscription["current_start"]
        )
        user.subscription_current_period_end = __import__("datetime").datetime.fromtimestamp(
            subscription["current_end"]
        )
        
        # Update limits based on plan
        limits = get_plan_limits(plan)
        user.videos_limit = limits["anime_videos"] + limits["realistic_videos"]
        
        await db.commit()
        logger.info(f"User {user_id} upgraded to {plan}")
        
    except Exception as e:
        logger.error(f"Failed to update user subscription: {e}")
        await db.rollback()


async def _handle_subscription_cancelled(payload: dict, db: AsyncSession):
    """Handle subscription cancellation"""
    subscription = payload["payload"]["subscription"]["entity"]
    notes = subscription.get("notes", {})
    
    user_id = notes.get("user_id")
    
    if not user_id:
        return
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user:
        user.subscription_status = "cancelled"
        # Don't downgrade immediately - let them use until period end
        await db.commit()
        logger.info(f"User {user_id} subscription cancelled")


async def _handle_payment_failed(payload: dict, db: AsyncSession):
    """Handle failed payment"""
    payment = payload["payload"]["payment"]["entity"]
    logger.warning(f"Payment failed: {payment.get('id')}")
    # Could notify user, retry logic, etc.


@router.get("/subscription")
async def get_subscription(
    current_user: User = Depends(get_current_active_user),
):
    """Get current user's subscription details"""
    return {
        "tier": current_user.tier.value,
        "status": current_user.subscription_status,
        "current_period_start": current_user.subscription_current_period_start.isoformat() if current_user.subscription_current_period_start else None,
        "current_period_end": current_user.subscription_current_period_end.isoformat() if current_user.subscription_current_period_end else None,
        "videos_used": current_user.videos_generated_this_month,
        "videos_limit": current_user.videos_limit,
        "remaining_videos": current_user.get_remaining_videos(),
    }