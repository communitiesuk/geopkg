import fiona
from geopkg.model.geocode import GeoCode
from fiona.model import to_dict
import os 
from pathlib import Path
from dataclasses import dataclass, field
from typing import Union


def rename_keys(properties: dict[str, Union[int, str]]) -> dict[str, Union[int, str]]:
        _map = {
            "CD": "code",
            "NM": "name",
            "MW": "name_welsh",
        }

        return (
            {_map[k[-2:]] if k.endswith(tuple(_map.keys())) 
            else k.lower(): v for k,v in properties.items()}
        )


@dataclass
class GeoCodeLibrary:
    """

    """
    geocode_files: list[Path]
    years: list[int]
    geocodes: dict[str, GeoCode] = field(default_factory=dict, init=False)
       

    def load_geocodes(self) -> None:
        for file in self.geocode_files:
            with fiona.open(file) as layer:
                for feature in layer:
                    properties = to_dict(feature.properties)
                    properties = rename_keys(properties)
                    self.geocodes[properties["code"]] = GeoCode(year=years[0],geometry=feature.geometry, **properties)


if __name__ == "__main__":
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    files = [dir_path/"Local_Authority_Districts_2023_May.gpkg"]
    years = [2023]

    a = GeoCodeLibrary(files, years)
    a.load_geocodes()

    for x, y in a.geocodes.items():
        print (y.year, y.code)

