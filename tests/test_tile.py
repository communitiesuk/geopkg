import pytest

from geopkg.tile import calculate_latitude, calculate_longitude
from geopkg.types import Coordinate, Vector


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
