from enum import Enum

from geopkg.types import BoundingBox

GEOMETRY_COLUMN_NAME = "geometry"
REQUIRED_COLUMNS: tuple[str, ...] = GEOMETRY_COLUMN_NAME, "code", "name", "welsh_name"

DEFAULT_MAX_ZOOM = 14


class CoordinateReferenceSystem(Enum):
    WGS84 = 4326
    WEB_MERCATOR = 3857


UK_BBOX = BoundingBox(
    east=1.9167,
    north=60.8333,
    south=49.8333,
    west=-8.1667,
)


class GeoType(Enum):
    REGION = "region"
    LAD = "lad"
    LSOA = "lsoa"
    MSOA = "msoa"
    OA = "oa"
