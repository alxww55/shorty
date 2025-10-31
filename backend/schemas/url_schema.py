from datetime import UTC, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
)


class ShortenedURLBase(BaseModel):
    original_url: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Original URL",
        alias="originalUrl",
    )
    expires_at: datetime | None = Field(
        None,
        description="Shortened URL expires at",
        alias="shortenedUrlExpiresAt",
    )

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=None
    )

    @field_validator("expires_at")
    def validate_expires_at(cls, value: datetime | None) -> datetime | None:
        if value is not None and value < datetime.now(UTC):
            raise ValidationError("expires_at cannot be in the past")
        return value


class ShortenedURLCreate(ShortenedURLBase):
    pass


class ShortenedURLResponse(ShortenedURLBase):
    id: int = Field(
        ..., description="Unique URL id", alias="uniqueShortenedUrlIdentifier"
    )
    shortened_url: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Shortened URL",
        alias="shortenedUrl",
    )
    created_at: datetime = Field(
        ..., description="URL created at", alias="shortenedUrlCreatedAt"
    )
