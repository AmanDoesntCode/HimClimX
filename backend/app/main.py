from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .api.analyze import router as analyze_router
from .api.forecast import router as forecast_router
from .api.meta import router as meta_router
from .core.errors import register_exception_handlers
from .core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="HimClimX Backend",
    version="0.2.0",
    default_response_class=ORJSONResponse,
)

register_exception_handlers(app)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(meta_router)
app.include_router(analyze_router)
app.include_router(forecast_router)
