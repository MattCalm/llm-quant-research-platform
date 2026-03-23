"""Application configuration module.

This module defines strongly-typed environment-backed settings for the MVP.
The goal is to keep config explicit and interview-friendly.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables.

    TODO(phase1): lock down additional operational settings (timeouts, limits).
    """

    app_name: str = "llm-quant-research-platform"
    environment: str = Field(default="dev")
    log_level: str = Field(default="INFO")

    llm_provider: str = Field(default="mock", description="mock|openai")
    llm_model: str = Field(default="gpt-4o-mini")
    openai_api_key: str | None = None
    llm_max_retries: int = Field(default=2, ge=0, le=5)

    data_period: str = Field(default="2y")
    signal_threshold: float = Field(default=0.2)
    sentiment_weight: float = Field(default=0.4, ge=0, le=1)
    technical_weight: float = Field(default=0.6, ge=0, le=1)

    model_config = SettingsConfigDict(env_file=".env", env_prefix="LQRP_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return a cached singleton settings object."""
    return Settings()
