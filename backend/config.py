from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    description: str
    version: str
    api_prefix: str
    static_dir: str

    debug: bool

    database_url: str
    cors_origins: list[str]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
