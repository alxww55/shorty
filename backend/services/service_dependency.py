from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import db_helper
from .url_service import URLService


async def get_url_service(
    session: AsyncSession = Depends(db_helper.session_dependency),  # noqa: B008
):
    return URLService(session)
