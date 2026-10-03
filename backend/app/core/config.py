"""Application configuration loaded from environment / .env."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")

    # Database
    database_url: str = "sqlite:///./data/citrusguard.db"

    # Auth
    jwt_secret: str = "change-me-to-a-long-random-string-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 720

    # CORS
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Uploads
    max_upload_mb: int = 10
    upload_dir: str = "./data/uploads"

    # Demo
    demo_mode: bool = True

    # Logging
    log_level: str = "INFO"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
