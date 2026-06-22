from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.cost_estimate import CostEstimate
from app.schemas.cost import CostEstimateCreate, CostEstimateResponse

router = APIRouter()


@router.post("", response_model=CostEstimateResponse, status_code=201)
async def create_cost_estimate(
    body: CostEstimateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    estimate = CostEstimate(
        project_id=body.project_id,
        user_id=current_user.id,
        total_cost=body.total_cost,
        currency=body.currency,
        breakdown_json=body.breakdown_json,
    )
    db.add(estimate)
    await db.flush()
    await db.refresh(estimate)
    return estimate


@router.get("", response_model=list[CostEstimateResponse])
async def list_cost_estimates(
    project_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(CostEstimate).where(CostEstimate.user_id == current_user.id)
    if project_id is not None:
        stmt = stmt.where(CostEstimate.project_id == project_id)
    stmt = stmt.order_by(CostEstimate.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/{estimate_id}", response_model=CostEstimateResponse)
async def get_cost_estimate(
    estimate_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(CostEstimate).where(
            CostEstimate.id == estimate_id,
            CostEstimate.user_id == current_user.id,
        )
    )
    estimate = result.scalar_one_or_none()
    if not estimate:
        raise HTTPException(status_code=404, detail="Cost estimate not found")
    return estimate


@router.delete("/{estimate_id}", status_code=204)
async def delete_cost_estimate(
    estimate_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(CostEstimate).where(
            CostEstimate.id == estimate_id,
            CostEstimate.user_id == current_user.id,
        )
    )
    estimate = result.scalar_one_or_none()
    if not estimate:
        raise HTTPException(status_code=404, detail="Cost estimate not found")
    await db.delete(estimate)
    await db.flush()
