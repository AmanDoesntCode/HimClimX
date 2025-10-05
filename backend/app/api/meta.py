from pathlib import Path

from fastapi import APIRouter

from ..api.models import Region, Variable
from ..services.data_loader import _shp_dir, list_available_variables

router = APIRouter(prefix="/meta", tags=["Metadata"])


@router.get("/variables", response_model=list[Variable])
def get_variables():
    """
    Dynamically list variables available in the NetCDF dataset directory.
    Scans the folder defined by NETCDF_PATH in .env.
    """
    ids = list_available_variables()

    # quick metadata map (you can expand this later from YAML or DB)
    name_map = {
        "tmp": ("Mean Temperature", "°C"),
        "tmn": ("Minimum Temperature", "°C"),
        "tmx": ("Maximum Temperature", "°C"),
        "pre": ("Precipitation", "mm"),
        "vap": ("Vapour Pressure", "hPa"),
        "cld": ("Cloud Cover", "%"),
        "dtr": ("Diurnal Temp Range", "°C"),
        "frs": ("Frost Days", "days"),
        "wet": ("Wet Days", "days"),
        "pet": ("Potential Evapotranspiration", "mm"),
    }

    return [
        Variable(
            id=i,
            name=name_map.get(i, (i.upper(), None))[0],
            units=name_map.get(i, (None, None))[1],
            description=None,
        )
        for i in ids
    ]


@router.get("/regions", response_model=list[Region])
def get_regions():
    """
    List region shapefiles available in the shapefile directory.
    Reads filenames (e.g., W2000.shp → id='W2000').
    """
    shp_dir = _shp_dir()
    shapefiles = list(Path(shp_dir).glob("*.shp"))
    regions = []
    for f in shapefiles:
        region_id = f.stem
        regions.append(
            Region(
                id=region_id,
                name=region_id,
                bbox=None,  # we can compute bounding boxes later
            )
        )
    return regions
