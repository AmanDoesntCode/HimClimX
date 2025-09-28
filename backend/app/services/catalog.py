import time
from typing import Any

from ..api.models import Region, Variable
from ..core.config import get_settings

# Simple in-memory cache
_cache: dict[str, tuple[float, Any]] = {}


def _get_cached(key: str, ttl: int):
    now = time.time()
    hit = _cache.get(key)
    if hit and now - hit[0] < ttl:
        return hit[1]
    return None


def _set_cache(key: str, value: Any):
    _cache[key] = (time.time(), value)


def list_variables() -> list[Variable]:
    ttl = get_settings().CACHE_TTL_SECONDS
    if (v := _get_cached("variables", ttl)) is not None:
        return v
    # Minimal starter set; replace with real scan in Phase 2
    data = [
        Variable(id="tavg", name="Average Temperature", units="°C"),
        Variable(id="prcp", name="Precipitation", units="mm"),
        Variable(id="tmin", name="Minimum Temperature", units="°C"),
        Variable(id="tmax", name="Maximum Temperature", units="°C"),
    ]
    _set_cache("variables", data)
    return data


def list_regions() -> list[Region]:
    ttl = get_settings().CACHE_TTL_SECONDS
    if (r := _get_cached("regions", ttl)) is not None:
        return r
    data = [
        Region(id="L1", name="Ladakh", bbox=(76.0, 32.0, 79.5, 35.2)),
        Region(id="HK", name="Himachal–Kinnaur", bbox=(76.0, 30.5, 78.5, 32.7)),
        Region(id="UK", name="Uttarakhand", bbox=(77.5, 29.0, 81.0, 31.5)),
    ]
    _set_cache("regions", data)
    return data


def get_variable_or_404(var_id: str) -> Variable | None:
    return next((v for v in list_variables() if v.id.lower() == var_id.lower()), None)


def get_region_or_404(region_id: str) -> Region | None:
    return next((r for r in list_regions() if r.id.lower() == region_id.lower()), None)
