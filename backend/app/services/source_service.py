from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repository import BaseRepository
from app.models.source import Source, ContentSource, SourceType, ContentType
from app.schemas.source import SourceCreate, SourceUpdate, ContentSourceCreate


class SourceRepository(BaseRepository[Source]):
    def __init__(self, db: AsyncSession):
        super().__init__(Source, db)


class ContentSourceRepository(BaseRepository[ContentSource]):
    def __init__(self, db: AsyncSession):
        super().__init__(ContentSource, db)


class SourceService:
    """Manages content sources and attribution."""

    PRIORITY_ORDER = [
        SourceType.WIKIPEDIA,
        SourceType.ELECTRONICS_TUTORIALS,
        SourceType.ARDUINO_DOCS,
        SourceType.RASPBERRY_PI_DOCS,
        SourceType.SPARKFUN,
        SourceType.ADAFRUIT,
        SourceType.OPEN_SOURCE_CIRCUIT,
        SourceType.DATASHEET,
        SourceType.WIKIPEDIA_COMMONS,
        SourceType.WIKIMEDIA_COMMONS,
    ]

    def __init__(self, db: AsyncSession):
        self.db = db
        self.source_repo = SourceRepository(db)
        self.content_source_repo = ContentSourceRepository(db)

    # ── Source CRUD ─────────────────────────────────────────────

    async def create_source(self, data: SourceCreate) -> Source:
        return await self.source_repo.create(**data.model_dump())

    async def get_source(self, source_id: int) -> Source | None:
        return await self.source_repo.get(source_id)

    async def get_sources_by_type(self, source_type: SourceType, limit: int = 100) -> list[Source]:
        return await self.source_repo.get_multi(
            filters={"source_type": source_type.value, "is_active": True},
            order_by=Source.priority,
            limit=limit,
        )

    async def get_priority_sources(self, limit: int = 10) -> list[Source]:
        """Get the highest-priority active sources."""
        stmt = (
            select(Source)
            .where(Source.is_active.is_(True))
            .order_by(Source.priority)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def search_sources(self, query: str, limit: int = 20) -> list[Source]:
        """Search sources by title or URL."""
        stmt = (
            select(Source)
            .where(Source.is_active.is_(True), Source.title.ilike(f"%{query}%"))
            .order_by(Source.priority)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update_source(self, source_id: int, data: SourceUpdate) -> Source | None:
        return await self.source_repo.update(source_id, **data.model_dump(exclude_none=True))

    async def delete_source(self, source_id: int) -> bool:
        return await self.source_repo.delete(source_id)

    # ── Content Attribution ─────────────────────────────────────

    async def attribute_content(
        self,
        content_type: ContentType,
        content_id: int,
        source_id: int,
        usage_context: str | None = None,
        attribution_text: str | None = None,
        image_url: str | None = None,
        relevance_score: float | None = None,
    ) -> ContentSource:
        """Link a source to a piece of generated content."""
        data = ContentSourceCreate(
            source_id=source_id,
            content_type=content_type.value,
            content_id=content_id,
            usage_context=usage_context,
            attribution_text=attribution_text,
            image_url=image_url,
            relevance_score=relevance_score,
        )
        return await self.content_source_repo.create(**data.model_dump())

    async def get_content_sources(
        self, content_type: ContentType, content_id: int
    ) -> list[ContentSource]:
        """Get all sources attributed to a specific content item."""
        return await self.content_source_repo.get_multi(
            filters={
                "content_type": content_type.value,
                "content_id": content_id,
            }
        )

    async def get_sources_for_content(
        self, content_type: ContentType, content_id: int
    ) -> list[Source]:
        """Get source details for a content item (with joins)."""
        stmt = (
            select(Source)
            .join(ContentSource, Source.id == ContentSource.source_id)
            .where(
                ContentSource.content_type == content_type.value,
                ContentSource.content_id == content_id,
            )
            .order_by(Source.priority)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_content_attributions(self, source_id: int) -> int:
        """Count how many times a source has been used."""
        stmt = (
            select(func.count())
            .select_from(ContentSource)
            .where(ContentSource.source_id == source_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    # ── Attribution Formatting ──────────────────────────────────

    def format_attribution(self, source: Source) -> str:
        """Generate a human-readable attribution string."""
        parts = [f"Source: {source.title}"]
        if source.author:
            parts.append(f"Author: {source.author}")
        if source.license:
            parts.append(f"License: {source.license}")
        parts.append(f"URL: {source.url}")
        return " | ".join(parts)

    def format_attribution_markdown(self, sources: list[Source]) -> str:
        """Generate markdown-formatted attribution block."""
        if not sources:
            return ""
        lines = ["---", "**Sources:**"]
        for s in sources:
            license_note = f" ({s.license})" if s.license else ""
            lines.append(f"- [{s.title}]({s.url}){license_note}")
        return "\n".join(lines)
