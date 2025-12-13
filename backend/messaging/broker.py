from taskiq_aio_pika import AioPikaBroker

from ..config import settings

broker: AioPikaBroker = AioPikaBroker(
    url=settings.rabbitmq_config.rabbitmq_url_safe
)
