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


@pytest.mark.parametrize(
    "c, expected",
    [
        (Coordinate(4, 1, 3), "2-0-2"),
        (Coordinate(32, 32, 6), "16-16-5"),
        (Coordinate(512, 512, 10), "256-256-9"),
        (Coordinate(16031, 12345, 18), "8015-6172-17"),
    ],
)
def test_parent(c: Coordinate, expected: str) -> None:
    assert Tile(c).parent.id == expected


@pytest.mark.parametrize(
    "c, expected",
    [
        (Coordinate(0, 0, 0), ["0-0-1", "1-0-1", "1-1-1", "0-1-1"]),
        (Coordinate(1, 0, 2), ["2-0-3", "3-0-3", "3-1-3", "2-1-3"]),
        (Coordinate(0, 1, 2), ["0-2-3", "1-2-3", "1-3-3", "0-3-3"]),
        (Coordinate(0, 0, 4), ["0-0-5", "1-0-5", "1-1-5", "0-1-5"]),
        (Coordinate(1, 1, 8), ["2-2-9", "3-2-9", "3-3-9", "2-3-9"]),
    ],
)
def test_children(c: Coordinate, expected: list[str]) -> None:
    assert [t.id for t in Tile(c).children] == expected


def test_global_tile() -> None:
    assert Tile(Coordinate(0, 0, 0)).parent.id == "0-0-0"
