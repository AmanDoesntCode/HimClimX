# backend/tests/conftest.py
from __future__ import annotations

from pathlib import Path

import pytest


def _has_files(p: Path, pattern: str) -> bool:
    return p.exists() and any(p.glob(pattern))


def data_available() -> bool:
    """Return True if both NetCDFs and shapefiles exist."""
    try:
        # Import here to avoid top-level reassignment (mypy-safe)
        from app.core.config import get_settings
    except Exception:
        return False

    s = get_settings()
    try:
        nc_dir = s.abs_path(s.NETCDF_PATH)
        shp_dir = s.abs_path(s.SHAPEFILE_PATH)
    except Exception:
        return False

    return _has_files(nc_dir, "*.nc") and _has_files(shp_dir, "*.shp")


skip_if_no_data = pytest.mark.skipif(
    not data_available(),
    reason="Integration data not present on CI (NetCDF/shapefiles missing).",
)
