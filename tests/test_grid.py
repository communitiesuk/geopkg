import pytest

from geopkg.grid import UK_VIEW, Grid
from geopkg.types import GeoType


def test_uk_level_grid() -> None:
    assert [*UK_VIEW.keys()] == ["tilename", "bbox"]


def test_grid_invalid_geotype() -> None:
    grid = Grid(tiles=[])
    with pytest.raises(KeyError):
        grid.generate("invalid")


def test_grid_single_geotype() -> None:
    grid = Grid(tiles=[])
    assert grid.generate("lad") == {"LAD": [UK_VIEW]}


def test_grid_multiple_geotypes() -> None:
    grid = Grid(tiles=[])
    assert grid.generate("lad", "lsoa") == {
        GeoType.LAD.name: [UK_VIEW],
        GeoType.LSOA.name: [],
    }
