from fastapi import APIRouter

from ..core.config import get_settings
from ..core.errors import RegionNotFound, VariableNotFound
from ..services.catalog import get_region_or_404, get_variable_or_404
from ..services.forecasting import forecast
from .models import ForecastRequest, ForecastResponse

router = APIRouter(tags=["forecast"])


@router.post("/forecast", response_model=ForecastResponse)
def post_forecast(payload: ForecastRequest):
    if not get_settings().ENABLE_PROPHET:
        # still allow a simple stub forecast in Phase 1; toggle behavior later if you prefer 403
        pass
    if not get_variable_or_404(payload.variable_id):
        raise VariableNotFound(payload.variable_id)
    if not get_region_or_404(payload.region_id):
        raise RegionNotFound(payload.region_id)
    return forecast(payload)
