from fastapi import APIRouter, Depends, status
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
    url_data: URLCreate,
    request: Request,
    service: URLService = Depends(get_url_service),  # noqa: B008
):
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
    return RedirectResponse(
        url_data.original_url, status_code=status.HTTP_302_FOUND
    )
