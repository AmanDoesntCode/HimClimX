from datetime import date

from pydantic import BaseModel, Field


class Variable(BaseModel):
    id: str
    name: str
    units: str | None = None
    description: str | None = None


class Region(BaseModel):
    id: str
    name: str
    # simple bbox for now (minx, miny, maxx, maxy)
    bbox: tuple[float, float, float, float] | None = None


class TimeRange(BaseModel):
    start: date = Field(..., description="inclusive")
    end: date = Field(..., description="inclusive")


class AnalyzeRequest(BaseModel):
    variable_id: str
    region_id: str
    time_range: TimeRange
    options: list[str] = []


class AnalyzeResponse(BaseModel):
    mean: float | None = None
    std: float | None = None
    trend_per_decade: float | None = None
    pct_change: float | None = None
    count: int = 0
    # keep a tiny series sample for UI previews
    series_sample: list[tuple[str, float]] = []
    quality: dict | None = None
    meta: dict | None = None


class ForecastRequest(BaseModel):
    variable_id: str
    region_id: str
    horizon_years: int = 3


class ForecastPoint(BaseModel):
    date: str
    yhat: float
    yhat_lower: float | None = None
    yhat_upper: float | None = None


class ForecastResponse(BaseModel):
    points: list[ForecastPoint]
    meta: dict | None = None
