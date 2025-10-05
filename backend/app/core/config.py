from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# ---------- .env discovery (walk upward) ----------


def _find_env(start: Path) -> Optional[Path]:
    """
    Walk upward from `start` until a `.env` is found, or root is reached.
    Returns the path to the `.env`, or None if not found.
    """
    cur = start
    while True:
        candidate = cur / ".env"
        if candidate.exists():
            return candidate
        if cur.parent == cur:
            return None  # hit filesystem root
        cur = cur.parent


_THIS_FILE = Path(__file__).resolve()
_ENV_PATH = _find_env(_THIS_FILE)
# Fallback repo root guess if .env isn't present (keeps things usable in CI)
_REPO_ROOT = (_ENV_PATH.parent if _ENV_PATH else _THIS_FILE.parents[2]).resolve()


# ---------- Settings ----------


class Settings(BaseSettings):
    # === Data paths (relative paths resolved against repo root) ===
    NETCDF_PATH: str = "data/climate"
    SHAPEFILE_PATH: str = "data/shapefiles"
    DEM_PATH: str = "data/dem.tif"

    # === External services ===
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"
    DATABASE_URL: Optional[str] = None
    SENTRY_DSN: Optional[str] = None

    # === App behavior ===
    SECRET_KEY: str = "change-me"
    ENABLE_3D: bool = False
    MAX_FORECAST_YEARS: int = 5

    # === Defaults for analysis/ops ===
    CACHE_TTL_SECONDS: int = 600
    LOG_LEVEL: str = "INFO"

    # Load the discovered .env (keys used as-is, no prefix)
    model_config = SettingsConfigDict(
        env_file=str(_ENV_PATH) if _ENV_PATH else None,
        env_prefix="",
    )

    # ---- Helpers ---------------------------------------------------
    def abs_path(self, path_str: str) -> Path:
        """
        Return an absolute Path.
        If `path_str` is relative, resolve it against the directory containing `.env`
        (i.e., the project root). If `.env` isn't present, resolve against a sane fallback.
        """
        p = Path(path_str)
        if not p.is_absolute():
            base = _ENV_PATH.parent if _ENV_PATH else _REPO_ROOT
            p = base / p
        return p.resolve()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


# ---------- Debug helpers (optional) ----------


def env_path_str() -> str:
    """String form of the loaded .env path (or '<none-found>')."""
    return str(_ENV_PATH) if _ENV_PATH else "<none-found>"


def repo_root_str() -> str:
    """String form of the repo root used for relative path resolution."""
    return str(_REPO_ROOT)
