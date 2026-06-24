from typing import cast
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.safety_report import SafetyReport
from app.schemas.safety import (
    SafetyReportCreate,
    SafetyReportUpdate,
    SafetyReportResponse,
    SafetyReportList,
)

router = APIRouter()


@router.post("", response_model=SafetyReportResponse, status_code=201)
async def create_safety_report(
    body: SafetyReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = SafetyReport(
        circuit_id=body.circuit_id,
        user_id=current_user.id,
        status=body.status,
        issues_json=body.issues_json,
        severity=body.severity,
        recommendations=body.recommendations,
    )
    db.add(report)
    await db.flush()
    await db.refresh(report)
    return report


@router.get("", response_model=SafetyReportList)
async def list_safety_reports(
    circuit_id: int | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(SafetyReport).where(SafetyReport.user_id == current_user.id)
    if circuit_id is not None:
        stmt = stmt.where(SafetyReport.circuit_id == circuit_id)
    stmt = stmt.order_by(SafetyReport.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    items = result.scalars().all()
    count_stmt = select(SafetyReport.id).where(SafetyReport.user_id == current_user.id)
    if circuit_id is not None:
        count_stmt = count_stmt.where(SafetyReport.circuit_id == circuit_id)
    total = len((await db.execute(count_stmt)).scalars().all())
    return SafetyReportList(items=cast(list[SafetyReportResponse], items), total=total)


@router.get("/{report_id}", response_model=SafetyReportResponse)
async def get_safety_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(SafetyReport).where(
            SafetyReport.id == report_id,
            SafetyReport.user_id == current_user.id,
        )
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Safety report not found")
    return report


@router.patch("/{report_id}", response_model=SafetyReportResponse)
async def update_safety_report(
    report_id: int,
    body: SafetyReportUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(SafetyReport).where(
            SafetyReport.id == report_id,
            SafetyReport.user_id == current_user.id,
        )
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Safety report not found")
    if body.status is not None:
        report.status = body.status
    if body.issues_json is not None:
        report.issues_json = body.issues_json
    if body.severity is not None:
        report.severity = body.severity
    if body.recommendations is not None:
        report.recommendations = body.recommendations
    await db.flush()
    await db.refresh(report)
    return report


@router.delete("/{report_id}", status_code=204)
async def delete_safety_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(SafetyReport).where(
            SafetyReport.id == report_id,
            SafetyReport.user_id == current_user.id,
        )
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Safety report not found")
    await db.delete(report)
    await db.flush()
