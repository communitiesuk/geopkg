from pydantic import BaseModel, ConfigDict
from fiona.model import Geometry
from typing import Any, Optional

class GeoCode(BaseModel):
    """
    Representation of a single geocode record. Uses the gpkg record
    to identify the definition (year, name, lat and long) of the code.
    The tile is calculated and appended to generate a single,
    comprehensive definition of the geocode. """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    year: int
    geometry: Geometry
    code: str 
    name: str
    name_welsh: str
    long: float
    lat: float
    tile: Optional[str] = None