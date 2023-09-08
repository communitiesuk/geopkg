from dataclasses import dataclass
from pathlib import Path
from typing import Union

import geopandas as gpd  # type: ignore
import pandas as pd

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
    welsh_name_field: str = ""

    def __post_init__(self) -> None:
        validate_geocode_gdf(
            self.geocode_gdf, self.code_field, self.name_field, self.welsh_name_field
        )

        self.geocode_gdf = self.geocode_gdf.rename(
            columns={
                self.code_field: "code",
                self.name_field: "name",
                self.welsh_name_field: "welsh_name",
            }
        )

    @property
    def geocodes(self) -> list[str]:
        return list(set(self.geocode_gdf["code"]))

    def map_code_to_tile(self) -> dict[str, Union[str, list[str]]]:
        tiles: gpd.GeoDataFrame = gpd.read_file("tiles.gpkg")  # type: ignore
        tiles["zoom"] = tiles["tile"].str.split("-", expand=True)[2]
        zooms: list[int] = list(set(tiles["zoom"]))

        intersect = pd.DataFrame(
            self.geocode_gdf.sjoin(tiles, predicate="intersects")  # type: ignore
            .groupby(["code", "name", "welsh_name", "tile", "zoom"])
            .size()
            .reset_index(name="count")[["code", "name", "welsh_name", "tile", "zoom"]]
        )

        ret_map: dict[str, Union[str, list[str]]] = {}
        for code in self.geocodes:
            code_data = intersect.loc[intersect["code"] == code]

            tile_data: dict[int, list[str]] = {}
            for zoom in zooms:
                tile_data[zoom] = list(
                    list(list(code_data.loc[code_data["zoom"] == zoom, "tile"]))
                )

            ret_map[code] = {  # type: ignore
                "year": self.year,
                "name": self.geocode_gdf.loc[
                    self.geocode_gdf["code"] == code, "name"
                ].values[0],
                "welsh_name": self.geocode_gdf.loc[
                    self.geocode_gdf["code"] == code, "welsh_name"
                ].values[0],
                "tiles": tile_data,
            }

        return ret_map


gdf = gpd.read_file(Path("geopkg/Local_Authority_Districts_2023_May.gpkg"))
output = GeoTiler(gdf, 2023, "LAD23CD", "LAD23NM", "LAD23NMW").map_code_to_tile()
print(output)
