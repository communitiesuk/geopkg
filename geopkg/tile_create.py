import math
from dataclasses import dataclass

from shapely import Polygon
from shapely.geometry import box


@dataclass
class BoundingBox:
    north: float
    south: float
    east: float
    west: float


def tile_lon(x: int, z: int) -> float:
    return x / math.pow(2.0, z) * 360.0 - 180


def tile_lat(y: int, z: int) -> float:
    return math.degrees(
        math.atan(math.sinh(math.pi - (2.0 * math.pi * y) / math.pow(2.0, z)))
    )


def tile_bbox(zoom: int, x: int, y: int) -> BoundingBox:
    return BoundingBox(
        north=tile_lat(y, zoom),
        south=tile_lat(y + 1, zoom),
        west=tile_lon(x, zoom),
        east=tile_lon(x + 1, zoom),
    )


def tile_to_geojson(tile: str) -> tuple[str, Polygon]:
    z, x, y = tile.split("/")
    bbox = tile_bbox(zoom=int(z), x=int(x), y=int(y))
    box_geom = box(bbox.west, bbox.south, bbox.east, bbox.north)
    return f"{y}-{x}-{z}", box_geom
