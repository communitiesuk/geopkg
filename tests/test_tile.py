from dataclasses import asdict

import pytest
from shapely.geometry import Polygon

from geopkg.tile import Tile, calculate_latitude, calculate_longitude
from geopkg.types.model import Coordinate, Vector


@pytest.mark.parametrize(
    "v, expected",
    [
        ((-1, 0, 0), -540.0),
        ((0, 0, 0), -180.0),
        ((1, 0, 0), 180.0),
        ((2, 0, 0), 540.0),
        ((0, 5, 0), -180.0),
        ((0, 0, 5), -180.0),
    ],
)
def test_calculate_longitude(v: Vector, expected: float) -> None:
    assert calculate_longitude(Coordinate(*v)) == expected


@pytest.mark.parametrize(
    "v, expected",
    [
        ((0, -1, 0), 89.99075251648904),
        ((0, 0, 0), 85.0511287798066),
        ((0, 1, 0), -85.0511287798066),
        ((0, 2, 0), -89.99075251648904),
        ((0, 12, 0), -90.0),
        ((0, 0, 5), 85.0511287798066),
    ],
)
def test_calculate_latitude(v: Vector, expected: float) -> None:
    assert calculate_latitude(Coordinate(*v)) == expected


@pytest.mark.parametrize(
    "c, expected",
    [
        (Coordinate(0, 0, 0), "0-0-0"),
        (Coordinate(1, 0, 0), "1-0-0"),
        (Coordinate(0, 1, 0), "0-1-0"),
        (Coordinate(0, 0, 1), "0-0-1"),
        (Coordinate(1, 1, 1), "1-1-1"),
    ],
)
def test_tile_id(c: Coordinate, expected: str) -> None:
    assert str(Tile(c)) == expected


@pytest.mark.parametrize(
    "c, expected",
    [
        (Coordinate(0, 0, 0), (85.0511287798066, -85.0511287798066, 180.0, -180.0)),
        (Coordinate(1, 0, 0), (85.0511287798066, -85.0511287798066, 540.0, 180.0)),
        (Coordinate(0, 1, 0), (-85.0511287798066, -89.99075251648904, 180.0, -180.0)),
        (Coordinate(0, 0, 1), (85.0511287798066, 0.0, 0.0, -180.0)),
        (Coordinate(1, 1, 1), (0.0, -85.0511287798066, 180.0, 0.0)),
    ],
)
def test_tile_bbox(c: Coordinate, expected: tuple[float, float, float, float]) -> None:
    bbox = Tile(c).bbox
    assert tuple(asdict(bbox).values()) == expected


@pytest.mark.parametrize(
    "c, expected",
    [
        (Coordinate(0, 0, 0), 5),
        (Coordinate(1, 0, 0), 5),
        (Coordinate(0, 1, 0), 5),
        (Coordinate(0, 0, 1), 5),
        (Coordinate(1, 1, 1), 5),
    ],
)
def test_tile_to_geojson(c: Coordinate, expected: int) -> None:
    assert isinstance(Tile(c).geometry(), Polygon)
    assert len(Tile(c).geometry().exterior.coords) == expected
