from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.marketplace import (
    MarketplaceListingCreate,
    MarketplaceListingUpdate,
    MarketplaceListingResponse,
    MarketplaceListingList,
)
from app.services.marketplace_service import MarketplaceService

router = APIRouter()


@router.post("", response_model=MarketplaceListingResponse, status_code=status.HTTP_201_CREATED)
async def create_listing(
    body: MarketplaceListingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MarketplaceService(db)
    return await service.create(current_user.id, body)


@router.get("", response_model=MarketplaceListingList)
async def list_listings(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MarketplaceService(db)
    items = await service.get_active(skip=skip, limit=limit)
    total = await service.count_active()
    return MarketplaceListingList(items=items, total=total)


@router.get("/{listing_id}", response_model=MarketplaceListingResponse)
async def get_listing(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = MarketplaceService(db)
    listing = await service.get(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@router.patch("/{listing_id}", response_model=MarketplaceListingResponse)
async def update_listing(
    listing_id: int,
    body: MarketplaceListingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MarketplaceService(db)
    listing = await service.get(listing_id)
    if not listing or listing.seller_id != current_user.id:
        raise HTTPException(status_code=404, detail="Listing not found")
    updated = await service.update(listing_id, body)
    if not updated:
        raise HTTPException(status_code=404, detail="Listing not found")
    return updated


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MarketplaceService(db)
    listing = await service.get(listing_id)
    if not listing or listing.seller_id != current_user.id:
        raise HTTPException(status_code=404, detail="Listing not found")
    await service.delete(listing_id)
