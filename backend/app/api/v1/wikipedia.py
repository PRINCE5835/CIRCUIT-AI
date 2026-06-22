"""Wikipedia knowledge API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.source import Source, SourceType
from app.services.wikipedia_service import wikipedia_service

router = APIRouter(prefix="/wikipedia", tags=["wikipedia"])


@router.get("/search")
async def wiki_search(
    q: str,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
):
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
    results = await wikipedia_service.search(q, limit=limit)
    if not results:
        return {"results": [], "message": "No Wikipedia results found"}
    return {"results": results, "total": len(results)}


@router.get("/component/{component_name:path}")
async def wiki_component_info(
    component_name: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    info = await wikipedia_service.get_component_info(component_name)
    if not info:
        raise HTTPException(
            status_code=404,
            detail=f"No Wikipedia info found for '{component_name}'",
        )

    try:
        existing = await db.execute(
            select(Source).where(Source.url == info["url"])
        )
        if not existing.scalar_one_or_none():
            db.add(Source(
                title=info["wikipedia_title"],
                url=info["url"],
                source_type=SourceType.WIKIPEDIA.value,
                priority=1,
                language="en",
                is_active=True,
            ))
            await db.flush()
    except Exception:
        pass

    return info


@router.get("/component/{component_name}/details")
async def wiki_component_details(
    component_name: str,
    current_user: User = Depends(get_current_user),
):
    info = await wikipedia_service.get_details(component_name)
    if not info:
        raise HTTPException(status_code=404, detail=f"No details found for '{component_name}'")
    return info
