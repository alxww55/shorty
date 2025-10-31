from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base_model import Base


class ShortenedURL(Base):
    original_url: Mapped[str] = mapped_column(index=True)
    shortened_url: Mapped[str] = mapped_column(
        unique=True, index=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
