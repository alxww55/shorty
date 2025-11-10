from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.url_model import URLModel
from ..schemas.url_schema import URLCreate


class URLRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_url_by_id(self, url_id: int) -> URLModel | None:
        return await self.session.get(URLModel, url_id)

    async def get_url_by_shortened_code(
        self, shortened_code: str
    ) -> URLModel | None:
        result: Result = await self.session.execute(
            select(URLModel).where(URLModel.shortened_code == shortened_code)
        )
        return result.scalar_one_or_none()

    async def create_url(self, url_data: URLCreate) -> URLModel:
        url = URLModel(**url_data.model_dump())
        self.session.add(url)
        await self.session.commit()
        await self.session.refresh(url)
        return url

    async def update_clicks_count(self, shortened_code: str) -> dict:
        result: Result = await self.session.execute(
            update(URLModel)
            .where(URLModel.shortened_code == shortened_code)
            .values(clicks=URLModel.clicks + 1)
        )
        await self.session.commit()
        if result:
            return {"updated": "true"}
        return {"updated": "false"}
