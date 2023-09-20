import importlib.metadata

from .constants import UK_BBOX, zoom
from .geotiler import create_tile_map
from .tile import Tile, generate_tiles
from .types import BoundingBox, Coordinate

__version__ = importlib.metadata.version(__package__ or __name__)

__all__ = [
    "UK_BBOX",
    "zoom",
    "BoundingBox",
    "Coordinate",
    "Tile",
    "generate_tiles",
    "create_tile_map",
]
