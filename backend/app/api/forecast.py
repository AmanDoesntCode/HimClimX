from fastapi import APIRouter, HTTPException

from ..api.models import ForecastRequest, ForecastResponse
from ..services import forecasting
from ..services.data_loader import list_available_variables

router = APIRouter(prefix="", tags=["Forecast"])


@router.post("/forecast", response_model=ForecastResponse)
def post_forecast(req: ForecastRequest) -> ForecastResponse:
    if req.variable_id not in set(list_available_variables()):
        raise HTTPException(status_code=404, detail="variable_not_found")
    return forecasting.forecast(req)
