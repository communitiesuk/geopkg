from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generator

import mercantile
from shapely import Polygon

from geopkg.constants import DEFAULT_MAX_ZOOM
from geopkg.tile.compute import calculate_latitude, calculate_longitude
from geopkg.types import BoundingBox, Coordinate


@dataclass
class Tile:
    coordinate: Coordinate

    @property
    def id(self) -> str:
        return "-".join(map(str, self.coordinate.vector))

    @property
    def bbox(self) -> BoundingBox:
        x, y, z = self.coordinate.vector

        return BoundingBox(
            north=calculate_latitude(self.coordinate),
            south=calculate_latitude(Coordinate(x, y + 1, z)),
            west=calculate_longitude(self.coordinate),
            east=calculate_longitude(Coordinate(x + 1, y, z)),
        )

    @property
    def parent(self) -> Tile:
        mt = mercantile.Tile(*self.coordinate.vector)

        if mt.z == 0:
            return GLOBAL_TILE

        return Tile(Coordinate(*mercantile.parent(mt)))

    @property
    def children(self) -> list[Tile]:
        mt = mercantile.Tile(*self.coordinate.vector)
        return [Tile(Coordinate(*c)) for c in mercantile.children(mt)]

    def geometry(self) -> Polygon:
        return Polygon(self.bbox.vertices, holes=None)

    def geojson(self) -> dict[str, Any]:
        return {
            "type": "Feature",
            "bbox": self.bbox.edges,
            "id": self.id,
            "geometry": self.geometry().__geo_interface__,
            "properties": {
                "title": f"XYz tile {self.id}",
            },
        }

    def __repr__(self) -> str:
        return self.id


GLOBAL_TILE = Tile(Coordinate(x=0, y=0, z=0))


def generate_tiles(bbox: BoundingBox, max_z: int = DEFAULT_MAX_ZOOM) -> list[Tile]:
    m_tiles: Generator[mercantile.Tile, Any, None] = mercantile.tiles(
        *bbox.edges, zooms=[*range(max_z + 1)]
    )
    return [Tile(Coordinate(*t)) for t in m_tiles]
