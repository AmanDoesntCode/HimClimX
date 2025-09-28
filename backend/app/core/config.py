from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Paths / data
    DATA_ROOT: str = "data"
    REGIONS_FILE: str | None = None

    # Behavior / flags
    CACHE_TTL_SECONDS: int = 300
    ENABLE_PROPHET: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"

    # pydantic-settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="HIMCLIMX_",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
