from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repository import BaseRepository
from app.models.marketplace_listing import MarketplaceListing
from app.schemas.marketplace import MarketplaceListingCreate, MarketplaceListingUpdate


class MarketplaceRepository(BaseRepository[MarketplaceListing]):
    def __init__(self, db: AsyncSession):
        super().__init__(MarketplaceListing, db)


class MarketplaceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = MarketplaceRepository(db)

    async def create(self, seller_id: int, data: MarketplaceListingCreate) -> MarketplaceListing:
        return await self.repo.create(seller_id=seller_id, **data.model_dump(exclude_unset=True))

    async def get(self, listing_id: int) -> MarketplaceListing | None:
        return await self.repo.get(listing_id)

    async def get_active(self, skip: int = 0, limit: int = 50) -> list[MarketplaceListing]:
        return await self.repo.get_multi(
            filters={"status": "active"},
            order_by=MarketplaceListing.created_at.desc(),
            skip=skip,
            limit=limit,
        )

    async def get_seller_listings(self, seller_id: int) -> list[MarketplaceListing]:
        return await self.repo.get_multi(filters={"seller_id": seller_id})

    async def update(
        self, listing_id: int, data: MarketplaceListingUpdate
    ) -> MarketplaceListing | None:
        return await self.repo.update(listing_id, **data.model_dump(exclude_unset=True))

    async def delete(self, listing_id: int) -> bool:
        return await self.repo.delete(listing_id)

    async def count_active(self) -> int:
        return await self.repo.count(filters={"status": "active"})
