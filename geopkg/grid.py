from dataclasses import dataclass
from typing import TypedDict

from geopkg.constants import GEO_TYPE_ZOOM_MAP, UK_BBOX
from geopkg.tile import Tile
from geopkg.types import GeoType


class GridTile(TypedDict):
    tilename: str
    bbox: dict[str, float]


UK_VIEW: GridTile = {"tilename": "uk", "bbox": UK_BBOX.as_dict()}


@dataclass
class Grid:
    tiles: list[Tile]

    def __post_init__(self) -> None:
        self.tiles = sorted(self.tiles, key=lambda t: t.coordinate.z)

    def generate(self, *geotypes: str) -> dict[str, list[GridTile]]:
        for g in geotypes:
            if GeoType[g.upper()] not in GEO_TYPE_ZOOM_MAP:
                raise ValueError(f"Unknown geotype: {g}")

        if len(geotypes) == 1:
            return {geotypes[0].upper(): [UK_VIEW]}

        out: dict[str, list[GridTile]] = {}
        national, *subs = geotypes

        for g in subs:
            z = GEO_TYPE_ZOOM_MAP[GeoType[g.upper()]]
            t_z = [t for t in self.tiles if t.coordinate.z == z]

            out[g.upper()] = [
                {"tilename": tile.id, "bbox": tile.bbox.as_dict()} for tile in t_z
            ]

        return {
            national.upper(): [UK_VIEW],
            **out,
        }
