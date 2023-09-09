from dataclasses import dataclass
from typing import NamedTuple


class Coordinate(NamedTuple):
    x: int
    y: int
    z: int

    @property
    def vector(self) -> tuple[int, int, int]:
        return self.x, self.y, self.z


@dataclass
class BoundingBox:
    north: float
    south: float
    east: float
    west: float
