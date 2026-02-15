from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Global configuration for the career platform backend."""

    PROJECT_NAME: str = "Kasbiy Tanlov Platformasi"
    API_V1_STR: str = "/api/v1"

    # --- Database ---
    DATABASE_URL: str = "postgresql+psycopg2://user:pass@localhost:5432/career_db"

    # --- Auth / Security ---
    JWT_SECRET: str = "CHANGE_ME"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_MIN: int = 60

    # Field-level encryption key (must be 32 bytes BEFORE base64).
    FIELD_KEY: str = "CHANGE_ME_32BYTE_KEY__________"

    # CORS
    BACKEND_CORS_ORIGINS: str = "*"  # comma separated in real env

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

