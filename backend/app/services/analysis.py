# backend/app/services/analysis.py
from __future__ import annotations

from datetime import date
from typing import Optional

import numpy as np
import pandas as pd

from ..api.models import AnalyzeRequest, AnalyzeResponse
from .data_loader import monthly_region_series


def _trend_per_decade(y: np.ndarray) -> float:
    """
    Linear trend expressed per decade.
    We fit y ~ a + b*x over monthly x=[0..n-1], then scale months → decade.
    """
    n = len(y)
    if n < 2:
        return 0.0
    x = np.arange(n, dtype=float)
    # robust to NaNs: drop pairs where y is nan
    mask = ~np.isnan(y)
    if mask.sum() < 2:
        return 0.0
    x = x[mask]
    y = y[mask]
    slope_month = np.polyfit(x, y, 1)[0]  # units per month
    return float(slope_month * 120.0)  # 120 months per decade


def _pct_change(y: np.ndarray) -> Optional[float]:
    if len(y) < 2:
        return None
    # first and last non-nan
    first_idx = np.flatnonzero(~np.isnan(y))
    if len(first_idx) == 0:
        return None
    start_val = y[first_idx[0]]
    end_val = y[np.flatnonzero(~np.isnan(y))[-1]]
    if start_val == 0:
        return None
    return float((end_val - start_val) / abs(start_val) * 100.0)


def _quality_flags(series: pd.Series) -> dict:
    """
    Simple data quality scoring to surface gaps/outliers:
      - completeness: fraction of non-null points
      - consistency: fraction of diffs within 5*std(diff)
      - validity: placeholder (Phase 2b: enforce physical/unit bounds)
      - overall: weighted composite
    """
    total = int(series.shape[0])
    present = int(series.notna().sum())
    completeness = present / total if total else 0.0

    diffs = series.diff().dropna()
    if len(diffs) >= 3:
        thr = max(diffs.std(ddof=1) * 5.0, 1e-6)
        consistency = float((diffs.abs() < thr).mean())
    else:
        consistency = 1.0

    validity = 0.99  # TODO(Phase 2b): per-variable physical range checks

    overall = 0.4 * completeness + 0.4 * consistency + 0.2 * validity
    return {
        "completeness": round(float(completeness), 3),
        "consistency": round(float(consistency), 3),
        "validity": round(float(validity), 3),
        "overall": round(float(overall), 3),
    }


def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    """
    Compute region-level stats over a monthly area-mean series from CRU:
      - mean, std
      - linear trend per decade
      - percent change from first→last
      - quality flags
      - preview sample (first 12 rows)
    """
    # Parse dates (ensure plain date objects)
    start = date.fromisoformat(req.time_range.start.isoformat())
    end = date.fromisoformat(req.time_range.end.isoformat())

    # Build monthly series from disk-backed data
    s = monthly_region_series(
        req.variable_id, req.region_id, (start, end)
    )  # pandas Series

    resp = AnalyzeResponse()
    resp.meta = {
        "variable_id": req.variable_id,
        "region_id": req.region_id,
        "freq": "monthly",
    }

    if s.empty:
        resp.count = 0
        resp.mean = None
        resp.std = None
        resp.trend_per_decade = None
        resp.pct_change = None
        resp.series_sample = []
        resp.quality = {
            "completeness": 0.0,
            "consistency": 0.0,
            "validity": 0.0,
            "overall": 0.0,
        }
        return resp

    y = s.values.astype(float)
    resp.count = int(np.sum(~np.isnan(y)))
    resp.mean = float(np.nanmean(y))
    resp.std = float(np.nanstd(y, ddof=1)) if np.sum(~np.isnan(y)) > 1 else 0.0
    resp.trend_per_decade = _trend_per_decade(y)
    resp.pct_change = _pct_change(y)

    # 12-point preview (for UI/debug)
    head = s.iloc[:12]
    resp.series_sample = [
        (ts.strftime("%Y-%m-%d"), float(val)) for ts, val in head.items()
    ]

    resp.quality = _quality_flags(s)
    return resp
