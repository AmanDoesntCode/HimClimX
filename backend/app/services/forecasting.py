from __future__ import annotations

from ..api.models import ForecastPoint, ForecastRequest, ForecastResponse


def forecast(req: ForecastRequest) -> ForecastResponse:
    # Phase-1 stub: linear projection with small uncertainty band
    start_year = 2025
    points: list[ForecastPoint] = []
    base = 12.0  # pretend current value
    slope = 0.05  # units/year

    for i in range(req.horizon_years):
        year = start_year + i + 1
        yhat = base + slope * (i + 1)
        band = 0.25 + 0.05 * i
        points.append(
            ForecastPoint(
                date=f"{year}-01-01",
                yhat=yhat,
                yhat_lower=yhat - band,
                yhat_upper=yhat + band,
            )
        )

    return ForecastResponse(
        points=points, meta={"variable_id": req.variable_id, "region_id": req.region_id}
    )
