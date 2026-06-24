from typing import cast
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.component import ComponentCreate, ComponentUpdate, ComponentResponse, ComponentList
from app.services.component_service import ComponentService

router = APIRouter()


@router.post("", response_model=ComponentResponse, status_code=status.HTTP_201_CREATED)
async def create_component(
    body: ComponentCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    service = ComponentService(db)
    return await service.create(body)


@router.get("", response_model=ComponentList)
async def list_components(
    query: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    service = ComponentService(db)
    if query:
        items = await service.search(query, limit=limit)
    else:
        items = await service.get_multi(skip=skip, limit=limit)
    total = await service.count()
    return ComponentList(items=cast(list[ComponentResponse], items), total=total)


@router.get("/{component_id}", response_model=ComponentResponse)
async def get_component(
    component_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = ComponentService(db)
    component = await service.get(component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    return component


@router.patch("/{component_id}", response_model=ComponentResponse)
async def update_component(
    component_id: int,
    body: ComponentUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    service = ComponentService(db)
    updated = await service.update(component_id, body)
    if not updated:
        raise HTTPException(status_code=404, detail="Component not found")
    return updated


@router.delete("/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_component(
    component_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    service = ComponentService(db)
    deleted = await service.delete(component_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Component not found")
