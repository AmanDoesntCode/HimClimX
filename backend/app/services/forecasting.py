# backend/app/services/forecasting.py
from __future__ import annotations

from datetime import date

import pandas as pd
from prophet import Prophet

from ..api.models import ForecastRequest, ForecastResponse
from ..core.config import get_settings
from .cache import get_json, set_json
from .data_loader import monthly_region_series


def _build_prophet() -> Prophet:
    """
    Configure a Prophet model suitable for monthly climate series.
    We keep it simple for now; tweak seasonality/mode later if needed.
    """
    return Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        seasonality_mode="additive",
    )


def _df_from_series(series: pd.Series) -> pd.DataFrame:
    """Convert monthly Pandas Series -> Prophet dataframe (ds, y)."""
    return pd.DataFrame(
        {
            "ds": series.index.to_pydatetime(),
            "y": series.values,
        }
    )


def forecast(req: ForecastRequest) -> ForecastResponse:
    """
    Prophet-only forecast for a (variable_id, region_id).
    Uses full historical CRU monthly series and projects N years ahead.
    """
    settings = get_settings()

    # 1) Validate horizon and cap by settings
    max_years = int(getattr(settings, "MAX_FORECAST_YEARS", 5))
    horizon_years = int(max(1, min(int(req.horizon_years), max_years)))
    horizon_months = horizon_years * 12

    # 2) Build full-history monthly series (start wide; CRU monthly goes from 1901)
    start = date(1901, 1, 1)
    end = date.today()
    series = monthly_region_series(req.variable_id, req.region_id, (start, end))

    if not series.empty:
        # Ensure index is datetime before formatting
        last_index = series.index[-1]
        if isinstance(last_index, tuple):
            # If index is a tuple, extract the first element (assumed to be date)
            last_index = last_index[0]
        last_date = pd.to_datetime(last_index).strftime("%Y-%m-%d")
        cache_key_data = {
            "variable_id": req.variable_id,
            "region_id": req.region_id,
            "horizon": horizon_years,
            "last": last_date,
        }

    # try to get cached response
    cached = get_json("forecast", **cache_key_data)
    if cached:
        print("⚡ Cache hit for forecast", cache_key_data)
        return ForecastResponse(**cached)

    if series.empty:
        return ForecastResponse(
            points=[],
            meta={
                "variable_id": req.variable_id,
                "region_id": req.region_id,
                "model": "prophet",
                "note": "no data",
            },
        )

    # 3) Prepare data for Prophet
    df = _df_from_series(series)

    # 4) Fit + predict (guard with a friendly error path)
    try:
        m = _build_prophet()
        m.fit(df)

        future = m.make_future_dataframe(periods=horizon_months, freq="MS")
        fcst = m.predict(future).tail(horizon_months)
    except Exception as e:  # keep API resilient
        return ForecastResponse(
            points=[],
            meta={
                "variable_id": req.variable_id,
                "region_id": req.region_id,
                "model": "prophet",
                "error": str(e),
            },
        )

    # 5) Shape response points
    points = [
        ForecastResponse.__annotations__["points"].__args__[0](
            date=d.strftime("%Y-%m-%d"),
            yhat=float(y),
            yhat_lower=float(ylo),
            yhat_upper=float(yhi),
        )
        for d, y, ylo, yhi in zip(
            fcst["ds"], fcst["yhat"], fcst["yhat_lower"], fcst["yhat_upper"]
        )
    ]

    resp = ForecastResponse(
        points=points,
        meta={
            "variable_id": req.variable_id,
            "region_id": req.region_id,
            "model": "prophet",
            "last_observation": pd.to_datetime(
                series.index[-1][0]
                if isinstance(series.index[-1], tuple)
                else series.index[-1]
            ).strftime("%Y-%m-%d"),
            "horizon_years": horizon_years,
        },
    )

    # store in cache
    set_json(resp.dict(), ttl=900, base="forecast", **cache_key_data)
    print("💾 Cache saved for forecast", cache_key_data)

    return resp

    # return ForecastResponse(
    #     points=points,
    #     meta={
    #         "variable_id": req.variable_id,
    #         "region_id": req.region_id,
    #         "model": "prophet",
    #         "last_observation": pd.to_datetime(series.index[-1][0] if isinstance(series.index[-1], tuple) else series.index[-1]).strftime("%Y-%m-%d"),
    #         "horizon_years": horizon_years,
    #     },
    # )
