from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, Form, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from ..schemas.url_schema import URLCreate, URLResponse
from ..services.service_dependency import get_url_service
from ..services.url_service import URLService

router = APIRouter(tags=["shorty"])


@router.post(
    "/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED
)
async def create_shortened_url(
    request: Request,
    original_url: str = Form(...),
    shortened_code: str = Form(...),
    expires_at: int = Form(...),
    service: URLService = Depends(get_url_service),  # noqa: B008
):
    url_data = URLCreate(
        original_url=original_url,
        shortened_code=shortened_code,
        clicks=0,
        expires_at=datetime.now(UTC) + timedelta(days=expires_at),
    )

    return await service.create_shortened_url(url_data)


@router.get(
    "/{short_code}",
    status_code=status.HTTP_200_OK,
)
async def redirect_on_original_url(
    short_code: str,
    service: URLService = Depends(get_url_service),  # noqa: B008
):
    url_data = await service.get_original_url_by_shortened_url(short_code)
    await service.update_clicks_count(short_code)
    return RedirectResponse(
        url_data.original_url, status_code=status.HTTP_302_FOUND
    )
