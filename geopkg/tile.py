import math
from dataclasses import asdict, dataclass

from shapely import Polygon  # type: ignore

from geopkg.types import BoundingBox, Coordinate


def calculate_longitude(c: Coordinate) -> float:
    return c.x / math.pow(2.0, c.z) * 360.0 - 180


def calculate_latitude(c: Coordinate) -> float:
    return math.degrees(
        math.atan(math.sinh(math.pi - (2.0 * math.pi * c.y) / math.pow(2.0, c.z)))
    )


@dataclass
class Tile:
    coordinate: Coordinate

    @property
    def bbox(self) -> BoundingBox:
        x, y, z = self.coordinate.vector

        return BoundingBox(
            north=calculate_latitude(self.coordinate),
            south=calculate_latitude(Coordinate(x, y + 1, z)),
            west=calculate_longitude(self.coordinate),
            east=calculate_longitude(Coordinate(x + 1, y, z)),
        )

    def to_geojson(self) -> "Polygon":
        minx, miny, maxx, maxy = asdict(self.bbox).values()
        coords = [(maxx, miny), (maxx, maxy), (minx, maxy), (minx, miny)]
        return Polygon(coords)  # type: ignore

    def __repr__(self) -> str:
        return "-".join(map(str, self.coordinate.vector))
