from fastapi import APIRouter

from ..core.errors import RegionNotFound, VariableNotFound
from ..services.analysis import analyze
from ..services.catalog import get_region_or_404, get_variable_or_404
from .models import AnalyzeRequest, AnalyzeResponse

router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
def post_analyze(payload: AnalyzeRequest):
    if not get_variable_or_404(payload.variable_id):
        raise VariableNotFound(payload.variable_id)
    if not get_region_or_404(payload.region_id):
        raise RegionNotFound(payload.region_id)
    return analyze(payload)
