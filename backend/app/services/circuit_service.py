from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repository import BaseRepository
from app.models.circuit import Circuit
from app.schemas.circuit import CircuitCreate, CircuitUpdate


class CircuitRepository(BaseRepository[Circuit]):
    def __init__(self, db: AsyncSession):
        super().__init__(Circuit, db)


class CircuitService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CircuitRepository(db)

    async def create(self, user_id: int, data: CircuitCreate) -> Circuit:
        return await self.repo.create(user_id=user_id, **data.model_dump(exclude_unset=True))

    async def get(self, circuit_id: int) -> Circuit | None:
        return await self.repo.get(circuit_id)

    async def get_by_project(self, project_id: int) -> list[Circuit]:
        return await self.repo.get_multi(filters={"project_id": project_id})

    async def get_user_circuits(
        self, user_id: int, skip: int = 0, limit: int = 50
    ) -> list[Circuit]:
        return await self.repo.get_multi(
            filters={"user_id": user_id},
            order_by=Circuit.updated_at.desc(),
            skip=skip,
            limit=limit,
        )

    async def update(self, circuit_id: int, data: CircuitUpdate) -> Circuit | None:
        return await self.repo.update(circuit_id, **data.model_dump(exclude_unset=True))

    async def delete(self, circuit_id: int) -> bool:
        return await self.repo.delete(circuit_id)
