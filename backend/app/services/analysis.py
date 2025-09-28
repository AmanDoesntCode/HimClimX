from __future__ import annotations

import numpy as np

from ..api.models import AnalyzeRequest, AnalyzeResponse


def _trend_per_decade(y: np.ndarray) -> float:
    # simple linear trend slope * years/decade
    x = np.arange(len(y))
    slope = np.polyfit(x, y, 1)[0] if len(y) >= 2 else 0.0
    return float(slope * 10.0)


def _pct_change(y: np.ndarray) -> float | None:
    if len(y) < 2 or y[0] == 0:
        return None
    return float((y[-1] - y[0]) / abs(y[0]) * 100.0)


def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    # Phase-1 stub: synth series (replace with xarray logic in Phase 2)
    # deterministic mini-series so tests are stable
    rng = np.random.default_rng(42)
    n = 24  # 24 months example
    series = np.linspace(10.0, 12.0, n) + rng.normal(0.0, 0.2, n)
    y = series.astype(float)

    resp = AnalyzeResponse()
    resp.mean = float(np.mean(y))
    resp.std = float(np.std(y, ddof=1))
    resp.trend_per_decade = _trend_per_decade(y)
    resp.pct_change = _pct_change(y)
    resp.count = int(len(y))

    # small sample as (iso_date, value); fake monthly dates
    resp.series_sample = [
        (f"2023-{(i % 12) + 1:02d}-01", float(val)) for i, val in enumerate(y[:12])
    ]
    resp.quality = {
        "completeness": 0.98,
        "consistency": 0.97,
        "validity": 0.99,
        "overall": 0.98,
    }
    resp.meta = {"variable_id": req.variable_id, "region_id": req.region_id}
    return resp
