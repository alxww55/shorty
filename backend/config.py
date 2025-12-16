from pydantic import AmqpDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int = 5432
    db_name: str

    # DB URL as Pydantic type
    @property
    def database_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=f"{self.db_name}",
        )

    # Safe DB URL represented as string for Alembic
    @property
    def database_url_safe(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class RabbitmqConfig(BaseSettings):
    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_host: str
    rabbitmq_port: int = 5672

    @property
    def rabbitmq_url(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            username=self.rabbitmq_user,
            password=self.rabbitmq_password,
            host=self.rabbitmq_host,
            port=self.rabbitmq_port,
        )

    @property
    def rabbitmq_url_safe(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}"


class LoggingCongig(BaseSettings):
    log_file_path: str
    rotation: str
    retention: str
    format: str


class Settings(BaseSettings):
    app_name: str
    description: str
    version: str
    api_prefix: str
    static_dir: str
    debug: bool
    cors_origins: list[str]

    db_config: DBConfig
    rabbitmq_config: RabbitmqConfig
    logging_config: LoggingCongig

    @property
    def database_url(self) -> PostgresDsn:
        return self.db_config.database_url

    @property
    def rabbitmq_url(self) -> AmqpDsn:
        return self.rabbitmq_config.rabbitmq_url

    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__"
    )


settings = Settings()  # type: ignore
