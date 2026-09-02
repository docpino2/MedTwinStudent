from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


def normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgresql+"):
        return database_url
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    return database_url


class Settings(BaseSettings):
    app_name: str = "MedTwin Student API"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://medtwin:medtwin@localhost:5432/medtwin"
    backend_cors_origins: str = "http://localhost:3000"
    backend_cors_origin_regex: str | None = r"https://.*\.lovable\.app"
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4.1-mini"
    init_db_on_startup: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @cached_property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]

    @cached_property
    def sqlalchemy_database_url(self) -> str:
        return normalize_database_url(self.database_url)


settings = Settings()
