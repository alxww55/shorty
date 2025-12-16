from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import db_helper
from .url_service import URLService


async def get_url_service(
    session: AsyncSession = Depends(db_helper.session_dependency),  # noqa: B008
):
    logger.info("URL Service requested as dependency")
    return URLService(session)
