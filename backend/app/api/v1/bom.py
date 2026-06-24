from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.project_component import ProjectComponent
from app.schemas.bom import BOMItemCreate, BOMItemUpdate, BOMItemResponse, BOMResponse

router = APIRouter()


async def _get_project_or_404(project_id: int, user_id: int, db: AsyncSession) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project or project.user_id != user_id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def _item_response(item: ProjectComponent) -> BOMItemResponse:
    return BOMItemResponse(
        id=item.id,
        project_id=item.project_id,
        component_id=item.component_id,
        quantity=item.quantity,
        notes=item.notes,
        created_at=item.created_at,
        component_name=item.component.name if item.component else None,
        component_category=item.component.category if item.component else None,
    )


@router.get("/{project_id}/bom", response_model=BOMResponse)
async def list_bom(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _get_project_or_404(project_id, current_user.id, db)
    result = await db.execute(
        select(ProjectComponent)
        .where(ProjectComponent.project_id == project_id)
        .order_by(ProjectComponent.id)
    )
    items = result.scalars().all()
    return BOMResponse(
        items=[_item_response(i) for i in items],
        total=len(items),
        project_id=project_id,
    )


@router.post("/{project_id}/bom", response_model=BOMItemResponse, status_code=201)
async def add_bom_item(
    project_id: int,
    body: BOMItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _get_project_or_404(project_id, current_user.id, db)
    existing = await db.execute(
        select(ProjectComponent).where(
            ProjectComponent.project_id == project_id,
            ProjectComponent.component_id == body.component_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Component already in BOM")
    item = ProjectComponent(
        project_id=project_id,
        component_id=body.component_id,
        quantity=body.quantity,
        notes=body.notes,
    )
    db.add(item)
    await db.flush()
    await db.refresh(item, ["component"])
    return _item_response(item)


@router.patch("/{project_id}/bom/{item_id}", response_model=BOMItemResponse)
async def update_bom_item(
    project_id: int,
    item_id: int,
    body: BOMItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _get_project_or_404(project_id, current_user.id, db)
    result = await db.execute(
        select(ProjectComponent).where(
            ProjectComponent.id == item_id,
            ProjectComponent.project_id == project_id,
        )
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="BOM item not found")
    if body.quantity is not None:
        item.quantity = body.quantity
    if body.notes is not None:
        item.notes = body.notes
    await db.flush()
    await db.refresh(item, ["component"])
    return _item_response(item)


@router.delete("/{project_id}/bom/{item_id}", status_code=204)
async def delete_bom_item(
    project_id: int,
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _get_project_or_404(project_id, current_user.id, db)
    result = await db.execute(
        select(ProjectComponent).where(
            ProjectComponent.id == item_id,
            ProjectComponent.project_id == project_id,
        )
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="BOM item not found")
    await db.delete(item)
    await db.flush()
