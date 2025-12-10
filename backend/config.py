from pydantic import PostgresDsn
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
            scheme="postgresql+psycopg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=f"/{self.db_name}",
        )

    # Safe DB URL represented as string for Alembic
    @property
    def database_url_safe(self) -> str:
        return f"postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class Settings(BaseSettings):
    app_name: str
    description: str
    version: str
    api_prefix: str
    static_dir: str
    debug: bool
    cors_origins: list[str]

    db_config: DBConfig

    @property
    def database_url(self) -> PostgresDsn:
        return self.db_config.database_url

    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__"
    )


settings = Settings()  # type: ignore
