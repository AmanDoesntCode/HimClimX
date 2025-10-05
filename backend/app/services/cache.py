# backend/app/services/cache.py
from __future__ import annotations

import hashlib
import json
from typing import Any, Optional

import redis

from ..core.config import get_settings

_client: Optional[redis.Redis] = None


def _get_client() -> Optional[redis.Redis]:
    """Lazily initialize Redis client from .env REDIS_URL."""
    global _client
    if _client is None:
        url = get_settings().REDIS_URL
        if not url:
            return None
        try:
            _client = redis.Redis.from_url(url, decode_responses=True)
        except Exception as e:
            print(f"⚠️ Redis init failed: {e}")
            _client = None
    return _client


def _make_key(base: str, **kwargs) -> str:
    """Generate a stable cache key with a hash for long parameter sets."""
    raw = json.dumps(kwargs, sort_keys=True)
    h = hashlib.md5(raw.encode()).hexdigest()[:8]
    return f"{base}:{h}"


def get_json(base: str, **kwargs) -> Optional[dict]:
    """Return cached JSON (dict) if found."""
    cli = _get_client()
    if not cli:
        return None
    key = _make_key(base, **kwargs)
    data = cli.get(key)
    return json.loads(data) if data else None


def set_json(obj: Any, ttl: int = 600, base: str = "cache", **kwargs) -> None:
    """Serialize and store a dict/object as JSON with TTL (seconds)."""
    cli = _get_client()
    if not cli:
        return
    key = _make_key(base, **kwargs)
    cli.setex(key, ttl, json.dumps(obj))
