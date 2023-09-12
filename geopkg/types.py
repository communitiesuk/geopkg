from dataclasses import dataclass
from typing import NamedTuple

Vector = tuple[int, int, int]


class Coordinate(NamedTuple):
    x: int
    y: int
    z: int

    @property
    def vector(self) -> Vector:
        return self.x, self.y, self.z


@dataclass
class BoundingBox:
    north: float
    south: float
    east: float
    west: float

    @property
    def edges(self) -> tuple[float, float, float, float]:
        return self.west, self.south, self.east, self.north
