from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.url_model import ShortenedURL
from ..schemas.url_schema import ShortenedURLCreate


class URLRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_shortened_url_by_id(
        self, url_id: int
    ) -> ShortenedURL | None:
        return await self.session.get(ShortenedURL, url_id)

    async def get_shortened_url_by_shortened_url(
        self, shortened_url: str
    ) -> ShortenedURL | None:
        result: Result = await self.session.execute(
            select(ShortenedURL).where(
                ShortenedURL.shortened_url == shortened_url
            )
        )
        return result.scalar_one_or_none()

    async def create_shortened_url(
        self, shortened_url_data: ShortenedURLCreate
    ) -> ShortenedURL:
        shortened_url = ShortenedURL(**shortened_url_data.model_dump())
        self.session.add(shortened_url)
        await self.session.commit()
        await self.session.refresh(shortened_url)
        return shortened_url
