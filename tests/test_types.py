from geopkg.types import Coordinate


def test_coordinate() -> None:
    c = Coordinate(1, 2, 3)
    assert c.x == 1
    assert c.y == 2
    assert c.z == 3
    assert c.vector == (1, 2, 3)
