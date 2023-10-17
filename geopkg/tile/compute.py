import math

from geopkg.types import Coordinate


def tiles_at_zoom(z: int) -> int:
    if z <= 1:
        return [1, 5][z]

    return int((math.pow(4, z + 1) - 1) / 3)


def calculate_longitude(c: Coordinate) -> float:
    return c.x / math.pow(2.0, c.z) * 360.0 - 180


def calculate_latitude(c: Coordinate) -> float:
    return math.degrees(
        math.atan(math.sinh(math.pi - (2.0 * math.pi * c.y) / math.pow(2.0, c.z)))
    )
