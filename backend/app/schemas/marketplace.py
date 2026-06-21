from datetime import datetime
from app.schemas.common import BaseSchema


class MarketplaceListingCreate(BaseSchema):
    component_id: int
    title: str
    description: str | None = None
    price: float
    currency: str = "USD"
    quantity: int = 1
    condition: str = "new"
    location: str | None = None


class MarketplaceListingUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    currency: str | None = None
    quantity: int | None = None
    condition: str | None = None
    location: str | None = None
    status: str | None = None


class MarketplaceListingResponse(BaseSchema):
    id: int
    seller_id: int
    component_id: int
    title: str
    description: str | None
    price: float
    currency: str
    quantity: int
    condition: str
    location: str | None
    status: str
    created_at: datetime
    updated_at: datetime


class MarketplaceListingList(BaseSchema):
    items: list[MarketplaceListingResponse]
    total: int
