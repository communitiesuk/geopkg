from geopandas import GeoDataFrame

from geopkg.constants import GEOMETRY_COLUMN_NAME
from geopkg.exceptions import InvalidGeoDataFrameStructure


def validate_geocode_gdf(
    geo: GeoDataFrame, code: str, name: str, welsh_name: str
) -> None:
    columns: tuple[str, ...] = GEOMETRY_COLUMN_NAME, code, name, welsh_name

    if missing := [*filter(lambda c: c not in geo.columns, columns)]:
        raise InvalidGeoDataFrameStructure(
            f"GeoDataFrame expected {missing} column(s) in addition to {geo.columns}"
        )
