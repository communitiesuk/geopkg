from typing import Optional

from geopandas import GeoDataFrame

from geopkg.constants import GEOMETRY_COLUMN_NAME
from geopkg.exceptions import InvalidGeoDataFrameStructure


def validate_geocode_gdf(
    geo: GeoDataFrame, code: str, name: str, welsh_name: Optional[str]
) -> None:

    columns: list[str] = [
        c for c in [GEOMETRY_COLUMN_NAME, code, name, welsh_name] if c is not None
    ]

    if missing := [*filter(lambda c: c not in geo.columns, columns)]:
        raise InvalidGeoDataFrameStructure(
            f"GeoDataFrame expected {missing} column(s) in addition to {geo.columns}"
        )
