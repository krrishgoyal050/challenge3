from functools import lru_cache
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Carbon Footprint Awareness Platform"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+asyncpg://carbon:carbon@db:5432/carbon"
    redis_url: str = "redis://redis:6379/0"
    jwt_secret_key: str = Field(default="change-me-in-production")
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 20
    refresh_token_days: int = 14
    gemini_api_key: str | None = None
    frontend_origin: AnyHttpUrl | str = "http://localhost:3000"
    sentry_dsn: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
