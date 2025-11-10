import re
from datetime import UTC, datetime

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

    @field_validator("expires_at")
    def validate_expires_at(cls, value: datetime | None) -> datetime | None:
        if value is not None and value < datetime.now(UTC):
            raise ValueError("Field expires_at cannot be in the past")
        return value

    @field_validator("shortened_code")
    def validate_shortened_code(cls, value: str) -> str:
        pattern = re.compile(r"[!@#$^*()+\[\]{}|\\;\"'<>,\s]")
        if re.search(pattern, value):
            raise ValueError("Allowed symbols are: ., %, &, :, /, -, _, ?")
        return value


class URLCreate(URLBase):
    pass


class URLResponse(URLBase):
    id: int = Field(..., description="Unique URL id")

    created_at: datetime = Field(..., description="URL created at")
