import importlib.metadata

from . import constants
from .geotiler import create_tile_map
from .tile import Tile, generate_tiles
from .types import Coordinate

__version__ = importlib.metadata.version(__package__ or __name__)

__all__ = ["constants", "Coordinate", "Tile", "generate_tiles", "create_tile_map"]
