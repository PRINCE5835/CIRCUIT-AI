import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.circuit import Circuit
from app.models.project_component import ProjectComponent

router = APIRouter()


@router.get("/projects/{project_id}/export")
async def export_project(
    project_id: int,
    fmt: str = "json",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.user_id == current_user.id,
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    circuits = (await db.execute(
        select(Circuit).where(Circuit.project_id == project_id)
    )).scalars().all()

    bom = (await db.execute(
        select(ProjectComponent)
        .where(ProjectComponent.project_id == project_id)
    )).scalars().all()

    data = {
        "project": {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "status": project.status,
            "is_public": project.is_public,
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None,
        },
        "circuits": [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "netlist": c.netlist,
                "schematic_data": c.schematic_data,
                "components_json": c.components_json,
            }
            for c in circuits
        ],
        "bom": [
            {
                "component_id": b.component_id,
                "quantity": b.quantity,
                "notes": b.notes,
            }
            for b in bom
        ],
    }

    if fmt == "json":
        return Response(
            content=json.dumps(data, indent=2, default=str),
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="project-{project_id}.json"'},
        )

    raise HTTPException(status_code=400, detail=f"Unsupported format: {fmt}")
