from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories.url_repository import URLRepository
from ..schemas.url_schema import URLCreate, URLResponse


class URLService:
    def __init__(self, session: AsyncSession) -> None:
        self.url_repository = URLRepository(session)

    async def get_original_url_by_id(self, url_id: int) -> URLResponse:
        response_url = await self.url_repository.get_url_by_id(url_id)

        if not response_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"URL with id {url_id} not found",
            )
        return URLResponse.model_validate(response_url)

    async def get_original_url_by_shortened_url(
        self, shortened_url: str
    ) -> URLResponse:
        response_url = await self.url_repository.get_url_by_shortened_code(
            shortened_url
        )

        if not response_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"URL with code {shortened_url} not found",
            )
        return URLResponse.model_validate(response_url)

    async def create_shortened_url(
        self, shortened_url_data: URLCreate
    ) -> URLResponse:
        while (
            await self.url_repository.get_url_by_shortened_code(
                shortened_url_data.shortened_code
            )
            is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Alias '{shortened_url_data.shortened_code}' is already taken. Try another one.",  # noqa: E501
            )
        shortened_url = await self.url_repository.create_url(
            shortened_url_data
        )
        return URLResponse.model_validate(shortened_url)

    async def update_clicks_count(self, shortened_code: str) -> dict:
        url_to_update = await self.url_repository.get_url_by_shortened_code(
            shortened_code
        )

        if not url_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"URL with code {shortened_code} cannot be updated",
            )

        updated_url = await self.url_repository.update_clicks_count(
            shortened_code
        )

        return updated_url
