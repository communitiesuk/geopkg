from contextlib import nullcontext as does_not_raise
from typing import Any

import pytest

from geopkg import zoom
from geopkg.types import BoundingBox, Coordinate, Zoom


def test_coordinate() -> None:
    c = Coordinate(1, 2, 3)
    assert c.x == 1
    assert c.y == 2
    assert c.z == 3
    assert c.vector == (1, 2, 3)


@pytest.fixture(name="bbox")
def fixture_bbox() -> BoundingBox:
    return BoundingBox(
        north=71.538800,
        south=18.776300,
        east=-66.885417,
        west=-178.217598,
    )


def test_bbox(bbox: BoundingBox) -> None:
    assert bbox.as_dict() == {
        "north": 71.538800,
        "south": 18.776300,
        "east": -66.885417,
        "west": -178.217598,
    }


def test_bbox_edges(bbox: BoundingBox) -> None:
    assert bbox.edges == (-178.217598, 18.7763, -66.885417, 71.5388)


@pytest.mark.parametrize(
    "z, expected",
    [
        (zoom[1], 1),
        (zoom[5], 5),
        (zoom[14], 14),
    ],
)
def test_zoom(z: Zoom, expected: int) -> None:
    assert z == expected


@pytest.mark.parametrize(
    "z, error",
    [
        (0, pytest.raises(IndexError)),
        (5, does_not_raise()),
        (20, pytest.raises(IndexError)),
    ],
)
def test_invalid_zoom(z: Zoom, error: Any) -> None:
    with error:
        _ = zoom[z]  # type: ignore
