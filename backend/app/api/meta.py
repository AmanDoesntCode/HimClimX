from fastapi import APIRouter

from ..services.catalog import list_regions, list_variables
from .models import Region, Variable

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/variables", response_model=list[Variable])
def get_variables():
    return list_variables()


@router.get("/regions", response_model=list[Region])
def get_regions():
    return list_regions()
