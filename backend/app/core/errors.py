from fastapi import FastAPI
from fastapi.responses import JSONResponse


class VariableNotFound(Exception):
    def __init__(self, var_id: str):
        self.var_id = var_id


class RegionNotFound(Exception):
    def __init__(self, region_id: str):
        self.region_id = region_id


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(VariableNotFound)
    async def _var_not_found(_, exc: VariableNotFound):
        return JSONResponse(
            status_code=404,
            content={"error": "variable_not_found", "variable_id": exc.var_id},
        )

    @app.exception_handler(RegionNotFound)
    async def _region_not_found(_, exc: RegionNotFound):
        return JSONResponse(
            status_code=404,
            content={"error": "region_not_found", "region_id": exc.region_id},
        )
