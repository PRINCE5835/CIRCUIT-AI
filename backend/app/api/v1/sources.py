from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.source import SourceType, ContentType
from app.schemas.source import (
    SourceCreate,
    SourceUpdate,
    SourceResponse,
    SourceList,
    ContentSourceCreate,
    ContentSourceResponse,
)
from app.services.source_service import SourceService

router = APIRouter()


@router.post("", response_model=SourceResponse, status_code=201)
async def create_source(
    data: SourceCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = SourceService(db)
    return await service.create_source(data)


@router.get("", response_model=SourceList)
async def list_sources(
    source_type: SourceType | None = Query(None),
    query: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    service = SourceService(db)
    if query:
        items = await service.search_sources(query, limit)
    elif source_type:
        items = await service.get_sources_by_type(source_type, limit)
    else:
        items = await service.source_repo.get_multi(skip=skip, limit=limit)
    total = await service.source_repo.count()
    return SourceList(items=[SourceResponse.model_validate(s) for s in items], total=total)


@router.get("/priority", response_model=list[SourceResponse])
async def priority_sources(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    service = SourceService(db)
    items = await service.get_priority_sources(limit)
    return [SourceResponse.model_validate(s) for s in items]


@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(source_id: int, db: AsyncSession = Depends(get_db)):
    service = SourceService(db)
    source = await service.get_source(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return SourceResponse.model_validate(source)


@router.patch("/{source_id}", response_model=SourceResponse)
async def update_source(
    source_id: int,
    data: SourceUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = SourceService(db)
    source = await service.update_source(source_id, data)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return SourceResponse.model_validate(source)


@router.delete("/{source_id}", status_code=204)
async def delete_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = SourceService(db)
    deleted = await service.delete_source(source_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Source not found")


# ── Content Attribution ───────────────────────────────────────


@router.post("/attributions", response_model=ContentSourceResponse, status_code=201)
async def create_attribution(
    data: ContentSourceCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    service = SourceService(db)
    result = await service.attribute_content(
        content_type=ContentType(data.content_type),
        content_id=data.content_id,
        source_id=data.source_id,
        usage_context=data.usage_context,
        attribution_text=data.attribution_text,
        image_url=data.image_url,
        relevance_score=data.relevance_score,
    )
    return ContentSourceResponse.model_validate(result)


@router.get("/attributions/{content_type}/{content_id}", response_model=list[SourceResponse])
async def get_content_sources(
    content_type: ContentType,
    content_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = SourceService(db)
    sources = await service.get_sources_for_content(content_type, content_id)
    return [SourceResponse.model_validate(s) for s in sources]
