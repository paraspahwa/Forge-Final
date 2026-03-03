"""
Avatar endpoints for both Anime and Realistic characters
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.logging import get_logger
from app.models.avatar import Avatar, CharacterType
from app.models.user import User
from app.schemas.avatar import AvatarCreate, AvatarUpdate, AvatarResponse, AvatarListResponse
from app.api.v1.endpoints.auth import get_current_active_user
from app.services.avatar import avatar_service

logger = get_logger(__name__)
router = APIRouter()


@router.post("/generate", response_model=AvatarResponse, status_code=status.HTTP_201_CREATED)
async def generate_avatar(
    avatar_data: AvatarCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Generate a new avatar with multiple expressions
    
    - Supports both 'anime' and 'realistic' character types
    - Generates 5 expressions by default (happy, sad, angry, surprised, neutral)
    - Stores images in cloud storage
    """
    # Check user limits
    result = await db.execute(
        select(func.count(Avatar.id)).where(
            Avatar.user_id == current_user.id,
            Avatar.status == "active"
        )
    )
    avatar_count = result.scalar()
    
    if avatar_count >= settings.MAX_CHARACTERS_PER_USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum {settings.MAX_CHARACTERS_PER_USER} avatars allowed. Please archive some.",
        )
    
    # Validate character type
    try:
        char_type = CharacterType(avatar_data.character_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid character_type. Must be 'anime' or 'realistic'",
        )
    
    # Generate expressions
    try:
        logger.info(f"Generating {char_type.value} avatar for user {current_user.id}")
        
        expression_urls = await avatar_service.generate_avatar_set(
            character_type=char_type,
            description=avatar_data.description,
            expressions=avatar_data.expressions,
            base_seed=avatar_data.seed,
        )
        
        logger.info(f"Generated {len(expression_urls)} expressions")
        
    except Exception as e:
        logger.error(f"Failed to generate avatar: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate avatar: {str(e)}",
        )
    
    # Create slug from name
    from slugify import slugify
    slug = slugify(avatar_data.name)
    
    # Check slug uniqueness and append number if needed
    base_slug = slug
    counter = 1
    while True:
        result = await db.execute(
            select(Avatar).where(Avatar.slug == slug, Avatar.user_id == current_user.id)
        )
        if not result.scalar_one_or_none():
            break
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    # Create avatar record
    avatar = Avatar(
        user_id=current_user.id,
        character_type=char_type,
        name=avatar_data.name,
        description=avatar_data.description,
        slug=slug,
        appearance=avatar_data.appearance or {},
        expressions=expression_urls,
        generation_prompt=avatar_data.description,
        generation_seed=avatar_data.seed,
    )
    
    db.add(avatar)
    await db.commit()
    await db.refresh(avatar)
    
    logger.info(f"Avatar created: {avatar.id} ({avatar.name})")
    
    return avatar.to_dict()


@router.get("/", response_model=AvatarListResponse)
async def list_avatars(
    character_type: Optional[str] = Query(None, regex="^(anime|realistic)$"),
    status: Optional[str] = Query("active", regex="^(active|archived|all)$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List user's avatars with filtering and pagination"""
    query = select(Avatar).where(Avatar.user_id == current_user.id)
    
    # Filter by character type
    if character_type:
        query = query.where(Avatar.character_type == character_type)
    
    # Filter by status
    if status != "all":
        query = query.where(Avatar.status == status)
    
    # Order by favorite first, then created
    query = query.order_by(Avatar.is_favorite.desc(), Avatar.created_at.desc())
    
    # Count total
    count_result = await db.execute(
        select(func.count(Avatar.id)).where(Avatar.user_id == current_user.id)
    )
    total = count_result.scalar()
    
    # Paginate
    query = query.offset((page - 1) * per_page).limit(per_page)
    
    result = await db.execute(query)
    avatars = result.scalars().all()
    
    return {
        "items": [avatar.to_dict() for avatar in avatars],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get("/{avatar_id}", response_model=AvatarResponse)
async def get_avatar(
    avatar_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get specific avatar details"""
    result = await db.execute(
        select(Avatar).where(
            Avatar.id == str(avatar_id),
            Avatar.user_id == current_user.id
        )
    )
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    return avatar.to_dict()


@router.put("/{avatar_id}", response_model=AvatarResponse)
async def update_avatar(
    avatar_id: UUID,
    updates: AvatarUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update avatar metadata"""
    result = await db.execute(
        select(Avatar).where(
            Avatar.id == str(avatar_id),
            Avatar.user_id == current_user.id
        )
    )
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    # Update fields
    if updates.name is not None:
        avatar.name = updates.name
        
        # Update slug if name changed
        from slugify import slugify
        avatar.slug = slugify(updates.name)
    
    if updates.description is not None:
        avatar.description = updates.description
    
    if updates.is_favorite is not None:
        avatar.is_favorite = updates.is_favorite
    
    if updates.status is not None:
        avatar.status = updates.status
    
    avatar.updated_at = __import__("datetime").datetime.utcnow()
    await db.commit()
    await db.refresh(avatar)
    
    return avatar.to_dict()


@router.delete("/{avatar_id}")
async def delete_avatar(
    avatar_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Soft delete an avatar"""
    result = await db.execute(
        select(Avatar).where(
            Avatar.id == str(avatar_id),
            Avatar.user_id == current_user.id
        )
    )
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    # Soft delete
    avatar.status = "deleted"
    await db.commit()
    
    return {"message": "Avatar deleted successfully"}


@router.post("/{avatar_id}/favorite")
async def toggle_favorite(
    avatar_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Toggle avatar favorite status"""
    result = await db.execute(
        select(Avatar).where(
            Avatar.id == str(avatar_id),
            Avatar.user_id == current_user.id
        )
    )
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    avatar.is_favorite = not avatar.is_favorite
    await db.commit()
    
    return {
        "message": f"Avatar {'added to' if avatar.is_favorite else 'removed from'} favorites",
        "is_favorite": avatar.is_favorite,
    }