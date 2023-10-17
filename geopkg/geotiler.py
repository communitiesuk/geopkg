import warnings
from dataclasses import dataclass
from typing import Optional, Union

import geopandas as gpd  # type: ignore
import pandas as pd

from geopkg import UK_BBOX
from geopkg.constants import DEFAULT_MAX_ZOOM
from geopkg.tile import generate_tiles
from geopkg.validators import validate_geocode_gdf


@dataclass
class GeoTiler:
    """Utility class that maps a given set of geography codes (9 character codes) to
    their corresponding UK map tiles. Covers map tiles up to zoom of 13. Required
    input required is:
    GeoDataFrame of codes to be mapped, year that the codes relate to, and the names
    of the code, name and welsh_name fields in the data.
    ------
    PARAMETERS
    geocode_gdf: GeoDataFrame
        9 character geography codes to be mapped. Requires code, name and geometry
        columns
    year: int
        The year that the geography codes are valid for
    code_field: str
        Name of the geography code field in the properties JSON block
    name_field: str
        Name of the geography name field in the properties JSON block
    welsh_name_field: str
        Name of the geography Welsh name field in the properties JSON block
    ------
    RETURNS \n
    dict[str, str | list[str]] \n
    Dictionary containing every unique geocode, its name, welsh_name and a list
    of all tiles the geocode intersects with
    """

    geocode_gdf: gpd.GeoDataFrame
    year: int
    code_field: str
    name_field: str
    welsh_name_field: Optional[str] = None

    def __post_init__(self) -> None:
        validate_geocode_gdf(
            self.geocode_gdf, self.code_field, self.name_field, self.welsh_name_field
        )

        columns = {
            self.code_field: "code",
            self.name_field: "name",
        }
        if self.welsh_name_field is not None:
            columns[self.welsh_name_field] = "welsh_name"

        self.geocode_gdf = gpd.GeoDataFrame(self.geocode_gdf.rename(columns=columns))

    @property
    def geocodes(self) -> list[str]:
        return list(set(self.geocode_gdf["code"]))

    def map_code_to_tile(
        self, max_zoom: int = DEFAULT_MAX_ZOOM
    ) -> dict[str, Union[str, list[str]]]:
        if max_zoom > 10:
            warnings.warn(
                "WARNING: zoom levels above 10 can take a significant amount \
                    of time to complete",
            )

        tiles = generate_tiles(UK_BBOX, max_zoom)
        tiles_gdf = gpd.GeoDataFrame(  # type: ignore
            data=[tile.id for tile in tiles],
            geometry=[tile.geometry() for tile in tiles],
            columns=["tile_id"],
            crs=4326,
        )

        intersect = pd.DataFrame(
            self.geocode_gdf.sjoin(tiles_gdf, predicate="intersects")  # type: ignore
            .groupby(["code", "tile_id"])
            .size()
            .reset_index(name="count")[["code", "tile_id"]]
        )

        intersect["zoom"] = intersect["tile_id"].str.split(  # type: ignore
            "-", expand=True
        )[2]
        zooms: list[int] = list(set(intersect["zoom"]))

        ret_map: dict[str, Union[str, list[str]]] = {}
        for code in self.geocodes:
            code_data = intersect.loc[intersect["code"] == code]

            tile_data: dict[int, list[str]] = {}
            for zoom in zooms:
                tile_data[zoom] = list(
                    code_data.loc[code_data["zoom"] == zoom, "tile_id"]
                )

            ret_map[code] = {  # type: ignore
                "year": self.year,
                "name": self.geocode_gdf.loc[
                    self.geocode_gdf["code"] == code, "name"
                ].values[0],
                "welsh_name": self.geocode_gdf.loc[
                    self.geocode_gdf["code"] == code, "welsh_name"
                ].values[0]
                if self.welsh_name_field is not None
                else "",
                "tiles": tile_data,
            }

        return ret_map


def create_tile_map(
    geocode_gdf: gpd.GeoDataFrame,
    max_zoom: int,
    year: int,
    code_field: str,
    name_field: str,
    welsh_name_field: Optional[str] = None,
) -> dict[str, Union[str, list[str]]]:
    geotiler = GeoTiler(
        geocode_gdf=geocode_gdf,
        year=year,
        code_field=code_field,
        name_field=name_field,
        welsh_name_field=welsh_name_field,
    )

    return geotiler.map_code_to_tile(max_zoom)
