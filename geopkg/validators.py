from geopandas import GeoDataFrame

from geopkg.exceptions import InvalidGeoDataFrameStructure


def validate_geocode_gdf(
    geo: GeoDataFrame, code: str, name: str, welsh_name: str
) -> None:

    if "geometry" not in geo.columns:
        raise InvalidGeoDataFrameStructure("Expects a 'Geometry' column")

    if code not in geo.columns:
        raise InvalidGeoDataFrameStructure(f"Expects a '{code}' column")

    if name not in geo.columns:
        raise InvalidGeoDataFrameStructure(f"Expects a '{name}' column")

    if welsh_name not in geo.columns:
        raise InvalidGeoDataFrameStructure(f"Expects a '{welsh_name}' column")
