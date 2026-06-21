from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repository import BaseRepository
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, db: AsyncSession):
        super().__init__(Project, db)


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ProjectRepository(db)

    async def create(self, user_id: int, data: ProjectCreate) -> Project:
        return await self.repo.create(user_id=user_id, **data.model_dump(exclude_unset=True))

    async def get(self, project_id: int) -> Project | None:
        return await self.repo.get(project_id)

    async def get_user_projects(
        self, user_id: int, skip: int = 0, limit: int = 50
    ) -> list[Project]:
        return await self.repo.get_multi(
            filters={"user_id": user_id},
            order_by=Project.updated_at.desc(),
            skip=skip,
            limit=limit,
        )

    async def count_user_projects(self, user_id: int) -> int:
        return await self.repo.count(filters={"user_id": user_id})

    async def update(self, project_id: int, data: ProjectUpdate) -> Project | None:
        return await self.repo.update(project_id, **data.model_dump(exclude_unset=True))

    async def delete(self, project_id: int) -> bool:
        return await self.repo.delete(project_id)
