from taskiq import TaskiqDepends

from ..services.service_dependency import get_url_service
from ..services.url_service import URLService
from .broker import broker


@broker.task(schedule=[{"cron": "* 4 * * *"}])
async def delete_expired_links(
    service: URLService = TaskiqDepends(get_url_service)  # noqa: B008
) -> dict[str, str | Exception]:
    return await service.delete_outdated_urls()
