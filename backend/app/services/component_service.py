from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repository import BaseRepository
from app.models.component import Component
from app.schemas.component import ComponentCreate, ComponentUpdate


class ComponentRepository(BaseRepository[Component]):
    def __init__(self, db: AsyncSession):
        super().__init__(Component, db)


class ComponentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ComponentRepository(db)

    async def create(self, data: ComponentCreate) -> Component:
        return await self.repo.create(**data.model_dump(exclude_unset=True))

    async def get(self, component_id: int) -> Component | None:
        return await self.repo.get(component_id)

    async def get_multi(self, skip: int = 0, limit: int = 100) -> list[Component]:
        return await self.repo.get_multi(skip=skip, limit=limit)

    async def search(self, query: str, limit: int = 20) -> list[Component]:
        stmt = (
            select(Component)
            .where(
                Component.name.ilike(f"%{query}%")
                | (Component.category.ilike(f"%{query}%"))
                | (Component.manufacturer.ilike(f"%{query}%"))
                | (Component.model_number.ilike(f"%{query}%"))
            )
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count(self) -> int:
        return await self.repo.count()

    async def update(self, component_id: int, data: ComponentUpdate) -> Component | None:
        return await self.repo.update(component_id, **data.model_dump(exclude_unset=True))

    async def delete(self, component_id: int) -> bool:
        return await self.repo.delete(component_id)
