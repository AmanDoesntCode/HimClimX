# app/services/data_loader.py
from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Dict, Tuple

import geopandas as gpd
import pandas as pd
import regionmask
import xarray as xr

from ..core.config import get_settings

# ----------------------------
# 1) Discover CRU NetCDF files
# ----------------------------

# Matches: cru_ts4.09.1901.2024.tmp.dat_himalaya_subset.nc  -> var="tmp"
_CRU_VAR_RE = re.compile(r"\.(?P<var>[a-z]{3})\.dat_.*\.nc$", re.IGNORECASE)


def _nc_dir():
    s = get_settings()
    return s.abs_path(s.NETCDF_PATH)


def _shp_dir():
    s = get_settings()
    return s.abs_path(s.SHAPEFILE_PATH)


def find_climate_files() -> Dict[str, Path]:
    """Return mapping {var_id -> Path} by scanning NETCDF_PATH."""
    out: Dict[str, Path] = {}
    for p in _nc_dir().glob("*.nc"):
        m = _CRU_VAR_RE.search(p.name)
        if m:
            out[m.group("var").lower()] = p
    return out


def list_available_variables() -> list[str]:
    """Return sorted list like ['tmp','tmx','tmn','pre', ...]."""
    return sorted(find_climate_files().keys())


# ----------------------------
# 2) Load region polygon (WGS84)
# ----------------------------

# app/services/data_loader.py


def load_region_polygon(region_id: str) -> gpd.GeoDataFrame:
    shp = _shp_dir() / f"{region_id}.shp"
    if not shp.exists():
        raise FileNotFoundError(f"Region shapefile not found: {shp}")

    gdf = gpd.read_file(shp)

    # If multiple features, dissolve to a single polygon
    if len(gdf) > 1:
        gdf = gdf.dissolve()

    # Normalize index and add a clean name column
    gdf = gdf.reset_index(drop=True)
    gdf["region_id"] = region_id

    # Ensure CRS is lon/lat
    gdf = gdf.to_crs(epsg=4326)
    return gdf


# ----------------------------
# 3) Open variable dataset
# ----------------------------


def open_var_da(var_id: str) -> xr.DataArray:
    """
    Open NetCDF for var_id and return a DataArray named 'value' with time/lat/lon.
    Chooses the correct data variable:
      1) exact name == var_id (e.g., 'tmp')
      2) otherwise, any var with dims including ('time','lat','lon')
    """
    files = find_climate_files()
    if var_id not in files:
        raise FileNotFoundError(f"No NetCDF for variable '{var_id}' under {_nc_dir()}")
    ds = xr.open_dataset(files[var_id])

    # 1) exact match
    if var_id in ds.data_vars:
        da = ds[var_id]
    else:
        # 2) heuristic: choose a 3D var with expected dims
        candidates = []
        for name, dv in ds.data_vars.items():
            dims = tuple(dv.dims)
            if set(("time", "lat", "lon")).issubset(dims):
                candidates.append(name)
        if not candidates:
            raise ValueError(
                f"No 3D (time,lat,lon) data variable found in {files[var_id].name}. "
                f"Available: {list(ds.data_vars)}"
            )
        # prefer the one with the most elements (robust if multiple like stn/mae)
        da_name = sorted(candidates, key=lambda n: ds[n].size, reverse=True)[0]
        da = ds[da_name]

    # sanity on coords
    for c in ("time", "lat", "lon"):
        if c not in da.coords and c not in ds.coords:
            raise ValueError(
                f"Expected coordinate '{c}' missing in {files[var_id].name}; "
                f"var selected: {da.name}, dims={da.dims}"
            )

    return da.rename("value")


# ----------------------------
# 4) Make monthly region series
# ----------------------------


def monthly_region_series(
    var_id: str,
    region_id: str,
    time_range: Tuple[date, date],
) -> pd.Series:
    """Return monthly area-mean series (Pandas) for (var, region, start..end)."""
    start, end = time_range
    da = open_var_da(var_id).sel(time=slice(str(start), str(end)))

    gdf = load_region_polygon(region_id)
    # regionmask will rasterize polygon over (lon, lat) grid for us
    reg = regionmask.from_geopandas(gdf, names="region_id", name="regions")
    mask2d = reg.mask(da.lon, da.lat)  # dims: lat, lon; NaN outside, 0 inside

    masked = da.where(mask2d.notnull(), drop=True)
    reduced = masked.mean(dim=("lat", "lon"), skipna=True)

    s = reduced.to_series().dropna()
    s.name = var_id
    return s
