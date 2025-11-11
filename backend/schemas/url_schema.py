import re
from datetime import UTC, datetime

from fastapi import HTTPException
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class URLBase(BaseModel):
    original_url: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Original URL",
    )
    shortened_code: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Shortened URL code",
    )
    clicks: int = Field(..., ge=0)
    expires_at: datetime = Field(
        ...,
        description="Shortened URL expires at",
        examples=[None],
    )

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=None
    )

    @field_validator("original_url")
    @classmethod
    def validate_original_url(cls, value: str) -> str:
        value = value.strip()
        url_pattern = re.compile(
            r"^https://[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"
            r"(:[0-9]{1,5})?(/[^\s]*)?$"
        )
        if not url_pattern.match(value):
            raise ValueError(
                "Invalid URL format. Only secure HTTPS URLs allowed."
            )
        return value

    @field_validator("shortened_code")
    @classmethod
    def validate_shortened_code(cls, value: str) -> str:
        value = value.strip()
        if not re.match(r"^[a-z0-9_-]+$", value):
            raise ValueError(
                "Only lowercase letters, numbers, hyphens and underscores allowed."  # noqa: E501
            )

        reserved_words = {"api", "admin", "docs", "static", "health", "status"}
        if value in reserved_words:
            raise ValueError(f"Invalid input, '{value}' is a reserved")

        return value

    @field_validator("clicks")
    @classmethod
    def validate_clicks(cls, value: int) -> int:
        if value is None or value <= 0:
            raise ValueError()
        return value

    @field_validator("expires_at")
    @classmethod
    def validate_expires_at(cls, value: datetime) -> datetime:
        if value is not None and value < datetime.now(UTC):
            raise ValueError("Field expires_at cannot be in the past.")
        return value


class URLCreate(URLBase):
    pass


class URLResponse(URLBase):
    id: int = Field(..., description="Unique URL id")

    created_at: datetime = Field(..., description="URL created at")
