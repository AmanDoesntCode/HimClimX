# backend/app/api/analyze.py
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..api.models import AnalyzeRequest, AnalyzeResponse
from ..services import analysis
from ..services.data_loader import list_available_variables

router = APIRouter(prefix="", tags=["Analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
def post_analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze a variable over a region and time window using real CRU data.

    Request body (AnalyzeRequest):
      - variable_id: one of the NetCDF variables found on disk (e.g., 'tmp', 'pre', ...)
      - region_id:   shapefile stem (e.g., 'W2000', 'E4000', ...)
      - time_range:  {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
      - options:     e.g., ["trend","quality"] (reserved for future toggles)

    Returns (AnalyzeResponse):
      - mean, std, trend_per_decade, pct_change, count
      - series_sample (first 12 month points)
      - quality (completeness/consistency/validity/overall)
      - meta (variable_id, region_id, freq)
    """
    # optional: validate variable against what actually exists on disk
    vars_on_disk = set(list_available_variables())
    if req.variable_id not in vars_on_disk:
        raise HTTPException(status_code=404, detail="variable_not_found")

    # delegate to the real analysis engine
    return analysis.analyze(req)
