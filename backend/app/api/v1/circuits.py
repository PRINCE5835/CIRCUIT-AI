from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.circuit import CircuitCreate, CircuitUpdate, CircuitResponse, CircuitList
from app.services.circuit_service import CircuitService

router = APIRouter()


@router.post("", response_model=CircuitResponse, status_code=status.HTTP_201_CREATED)
async def create_circuit(
    body: CircuitCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CircuitService(db)
    return await service.create(current_user.id, body)


@router.get("", response_model=CircuitList)
async def list_circuits(
    project_id: int | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CircuitService(db)
    if project_id:
        items = await service.get_by_project(project_id)
        return CircuitList(items=items, total=len(items))
    items = await service.get_user_circuits(current_user.id, skip=skip, limit=limit)
    return CircuitList(items=items, total=len(items))


@router.get("/{circuit_id}", response_model=CircuitResponse)
async def get_circuit(
    circuit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CircuitService(db)
    circuit = await service.get(circuit_id)
    if not circuit or circuit.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit


@router.patch("/{circuit_id}", response_model=CircuitResponse)
async def update_circuit(
    circuit_id: int,
    body: CircuitUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CircuitService(db)
    circuit = await service.get(circuit_id)
    if not circuit or circuit.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Circuit not found")
    updated = await service.update(circuit_id, body)
    if not updated:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return updated


@router.delete("/{circuit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_circuit(
    circuit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CircuitService(db)
    circuit = await service.get(circuit_id)
    if not circuit or circuit.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Circuit not found")
    await service.delete(circuit_id)
