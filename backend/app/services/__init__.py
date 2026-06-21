from typing import Any, Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base
from app.db.repository import BaseRepository
from app.core.exceptions import NotFoundException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.repo = BaseRepository(model, db)
        self.model = model

    async def create(self, schema: CreateSchemaType) -> ModelType:
        data = schema.model_dump(exclude_unset=True) if hasattr(schema, "model_dump") else schema
        return await self.repo.create(**data)

    async def get(self, id: int) -> ModelType:
        instance = await self.repo.get(id)
        if instance is None:
            raise NotFoundException(self.model.__name__, id)
        return instance

    async def get_multi(
        self, skip: int = 0, limit: int = 100, filters: dict | None = None, order_by: Any = None
    ) -> list[ModelType]:
        return await self.repo.get_multi(skip=skip, limit=limit, filters=filters, order_by=order_by)

    async def update(self, id: int, schema: UpdateSchemaType) -> ModelType:
        data = schema.model_dump(exclude_unset=True) if hasattr(schema, "model_dump") else schema
        instance = await self.repo.update(id, **data)
        if instance is None:
            raise NotFoundException(self.model.__name__, id)
        return instance

    async def delete(self, id: int) -> None:
        deleted = await self.repo.delete(id)
        if not deleted:
            raise NotFoundException(self.model.__name__, id)

    async def count(self, filters: dict | None = None) -> int:
        return await self.repo.count(filters=filters)
