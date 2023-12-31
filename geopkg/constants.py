from enum import Enum

from geopkg.types import GeoType, Zoom
from geopkg.types.model import BoundingBox

GEOMETRY_COLUMN_NAME = "geometry"
REQUIRED_COLUMNS: tuple[str, ...] = GEOMETRY_COLUMN_NAME, "code", "name", "welsh_name"

DEFAULT_MAX_ZOOM = 14

zoom = Zoom()


class CoordinateReferenceSystem(Enum):
    WGS84 = 4326
    WEB_MERCATOR = 3857


UK_BBOX = BoundingBox(
    east=1.9167,
    north=60.8333,
    south=49.8333,
    west=-8.1667,
)


GEO_TYPE_ZOOM_MAP: dict[GeoType, int] = {
    GeoType.REGION: zoom[1],
    GeoType.LAD: zoom[5],
    GeoType.MSOA: zoom[8],
    GeoType.LSOA: zoom[10],
    GeoType.OA: zoom[14],
}
