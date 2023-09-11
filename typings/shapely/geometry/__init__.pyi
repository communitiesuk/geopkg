from typing import Any, Optional, Sequence, TypedDict

from shapely.geometry.base import CAP_STYLE as CAP_STYLE
from shapely.geometry.base import JOIN_STYLE as JOIN_STYLE
from shapely.geometry.base import BaseGeometry as BaseGeometry
from shapely.geometry.collection import GeometryCollection as GeometryCollection
from shapely.geometry.geo import box as box
from shapely.geometry.geo import mapping as mapping
from shapely.geometry.geo import shape as shape
from shapely.geometry.linestring import LineString as LineString
from shapely.geometry.multilinestring import MultiLineString as MultiLineString
from shapely.geometry.multipoint import MultiPoint as MultiPoint
from shapely.geometry.multipolygon import MultiPolygon as MultiPolygon
from shapely.geometry.point import Point as Point
from shapely.geometry.polygon import LinearRing as LinearRing

# Patch `shapely.geometry.Polygon` stub for linter cohesion
# from .polygon import Polygon as Polygon

class TGeoInterface(TypedDict):
    type: str
    coordinates: tuple[tuple[float, float], ...]

class Polygon(BaseGeometry):  # type: ignore
    """
    A geometry type representing an area that is enclosed by a linear ring.

    A polygon is a two-dimensional feature and has a non-zero area. It may
    have one or more negative-space "holes" which are also bounded by linear
    rings. If any rings cross each other, the feature is invalid and
    operations on it may fail.

    Parameters
    ----------
    shell : sequence
        A sequence of (x, y [,z]) numeric coordinate pairs or triples, or
        an array-like with shape (N, 2) or (N, 3).
        Also can be a sequence of Point objects.
    holes : sequence
        A sequence of objects which satisfy the same requirements as the
        shell parameters above

    Attributes
    ----------
    exterior : LinearRing
        The ring which bounds the positive space of the polygon.
    interiors : sequence
        A sequence of rings which bound all existing holes.

    Examples
    --------
    Create a square polygon with no holes

    >>> coords = ((0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.))
    >>> polygon = Polygon(coords)
    >>> polygon.area
    1.0
    """

    def __new__(
        cls,
        shell: Optional[Sequence[Sequence[Any]]],
        holes: Optional[Sequence[Sequence[Any]]],
    ) -> Any: ...
    @property
    def exterior(self) -> Any: ...
    @property
    def interiors(self) -> list[Any]: ...
    @property
    def coords(self) -> None: ...
    @property
    def __geo_interface__(self) -> TGeoInterface: ...
    def svg(
        self,
        scale_factor: float = 1.0,
        fill_color: Optional[str] = None,
        opacity: Optional[float] = None,
    ) -> str: ...
    @classmethod
    def from_bounds(
        cls, xmin: float, ymin: float, xmax: float, ymax: float
    ) -> "Polygon": ...
