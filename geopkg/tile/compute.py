import math

from geopkg.types import Coordinate


def calculate_longitude(c: Coordinate) -> float:
    return c.x / math.pow(2.0, c.z) * 360.0 - 180


def calculate_latitude(c: Coordinate) -> float:
    return math.degrees(
        math.atan(math.sinh(math.pi - (2.0 * math.pi * c.y) / math.pow(2.0, c.z)))
    )
