"""
Authentication endpoints
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.logging import get_logger
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_refresh_token,
)
from app.models.user import User, UserTier
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    TokenRefresh,
    PasswordResetRequest,
)
from app.services.geoip import get_country_from_ip

logger = get_logger(__name__)
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None or not user.is_active:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user
    
    - Detects country from IP for PPP pricing
    - Creates free tier account
    - Sends welcome email (background task)
    """
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Detect country from IP
    client_ip = request.client.host if request.client else "127.0.0.1"
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    
    country = await get_country_from_ip(client_ip)
    
    # Create user
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        country_code=country,
        detected_country=country,
        detected_ip=client_ip,
        tier=UserTier.FREE,
        videos_limit=4,  # 3 anime + 1 realistic for free
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    logger.info(f"New user registered: {user.email} from {country}")
    
    # TODO: Send welcome email in background
    # background_tasks.add_task(send_welcome_email, user.email)
    
    return user.to_dict()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Authenticate user and return JWT token"""
    # Find user by email
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        # Increment failed login attempts (optional security feature)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()
    
    # Create tokens
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    
    logger.info(f"User logged in: {user.email}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict(),
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: TokenRefresh,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token using refresh token"""
    try:
        user_id = verify_refresh_token(refresh_data.refresh_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {str(e)}",
        )
    
    # Get user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    # Create new tokens
    access_token = create_access_token(subject=str(user.id))
    new_refresh_token = create_refresh_token(subject=str(user.id))
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict(),
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user.to_dict()


@router.put("/me", response_model=UserResponse)
async def update_me(
    updates: dict,  # Should use a proper Pydantic schema
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user profile"""
    # Update allowed fields
    allowed_fields = ["full_name", "preferred_character_type", "timezone"]
    
    for field in allowed_fields:
        if field in updates:
            setattr(current_user, field, updates[field])
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user.to_dict()


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """Logout user (client-side token deletion)"""
    # In stateless JWT, we don't need server-side logout
    # But we can add token to a blocklist if needed
    return {"message": "Successfully logged out"}


@router.post("/forgot-password")
async def forgot_password(
    request: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Request password reset"""
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    
    if user:
        # Generate reset token
        reset_token = create_access_token(
            subject=str(user.id),
            expires_delta=__import__("datetime").timedelta(hours=1),
        )
        
        # TODO: Send reset email
        # background_tasks.add_task(send_reset_email, user.email, reset_token)
        pass
    
    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: AsyncSession = Depends(get_db),
):
    """Reset password with token"""
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Update password
    user.hashed_password = get_password_hash(new_password)
    await db.commit()
    
    return {"message": "Password successfully reset"}