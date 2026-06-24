"""Add sources and content_sources tables for content attribution.

Aligns with current SQLAlchemy model definitions (String columns,
not MySQL ENUMs) to ensure create_all() and alembic produce the
same schema.
"""

from alembic import op
import sqlalchemy as sa

revision: str = "003"
down_revision: str | None = "002"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("url", sa.String(length=255), nullable=False),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("priority", sa.Integer(), server_default="5"),
        sa.Column("license", sa.String(length=255), nullable=True),
        sa.Column("author", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("language", sa.String(length=10), server_default="en"),
        sa.Column("is_active", sa.Boolean(), server_default="1"),
        sa.Column("last_validated_at", sa.DateTime(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url", name="uk_source_url"),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )

    op.create_index("idx_source_type", "sources", ["source_type"])
    op.create_index("idx_source_priority", "sources", ["priority"])
    op.create_index("idx_source_active", "sources", ["is_active"])

    op.create_table(
        "content_sources",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("content_type", sa.String(length=50), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column("usage_context", sa.String(length=255), nullable=True),
        sa.Column("attribution_text", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(length=255), nullable=True),
        sa.Column("relevance_score", sa.Float(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"], ondelete="CASCADE"),
        sa.UniqueConstraint(
            "source_id",
            "content_type",
            "content_id",
            name="uk_content_source",
        ),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
    )

    op.create_index("idx_content_type_id", "content_sources", ["content_type", "content_id"])
    op.create_index("idx_content_source", "content_sources", ["source_id", "content_type"])


def downgrade() -> None:
    op.drop_table("content_sources")
    op.drop_table("sources")
