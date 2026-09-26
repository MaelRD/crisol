"""Centralized configuration.

Every setting comes from environment variables prefixed with ``CRISOL_`` (or a
local ``.env`` file). Code never reads ``os.environ`` directly: it asks for
``get_settings()``, which makes configuration explicit and easy to override in tests.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["development", "test", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CRISOL_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "El Crisol"
    environment: Environment = "development"

    log_level: LogLevel = "INFO"
    log_format: Literal["text", "json"] = "text"

    api_host: str = "127.0.0.1"
    api_port: int = Field(default=8000, ge=1, le=65535)


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings (cached; call ``get_settings.cache_clear()`` in tests)."""
    return Settings()
