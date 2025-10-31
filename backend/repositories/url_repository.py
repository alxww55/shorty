from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.url_model import URLModel
from ..schemas.url_schema import URLCreate


class URLRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_url_by_id(self, url_id: int) -> URLModel | None:
        return await self.session.get(URLModel, url_id)

    async def get_url_by_shortened_url(
        self, shortened_url: str
    ) -> URLModel | None:
        result: Result = await self.session.execute(
            select(URLModel).where(URLModel.shortened_url == shortened_url)
        )
        return result.scalar_one_or_none()

    async def create_url(self, shortened_url_data: URLCreate) -> URLModel:
        shortened_url = URLModel(**shortened_url_data.model_dump())
        self.session.add(shortened_url)
        await self.session.commit()
        await self.session.refresh(shortened_url)
        return shortened_url
