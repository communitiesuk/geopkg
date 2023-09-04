import fiona
from geopkg.model.geocode import GeoCode
from geopkg.download.ref_data import RefData, reference_config
from fiona.model import to_dict
import os 
import itertools
from pathlib import Path
from dataclasses import dataclass, field
from typing import Union


@dataclass
class GeoCodeLibrary:
    """

    """
    geo_types: list[str]
    years: list[int]
    reference_data: dict[str, RefData] = field(default_factory=dict, init=False)
    geocodes: dict[str, GeoCode] = field(default_factory=dict, init=False)
    
    def __post_init__(self) -> None:
        for geo_type, years in reference_config.items():
            for year, config in years.items():
                self.reference_data[f"{geo_type}_{year}"] = RefData(config["filename"])

    @property
    def available_reference_data(self) -> None:
        return list(self.reference_data.keys())

    @property
    def requested_reference_data(self) -> None:
        comb_list = list(itertools.product(self.geo_types,self.years))
        return ["_".join(item) for item in comb_list]

    @property
    def missing_reference_data(self) -> None:
        return [ref_data for ref_data in self.requested_reference_data if ref_data in self.available_reference_data]

    def download_reference_data(self, ref_data: str) -> None:
        return self.reference_data[ref_data].download()

    def create_geo_code(self, data, year: str) -> None:

        def rename_properties(properties: dict[str, Union[int, str]]) -> dict[str, Union[int, str]]:
            _map = {
                "CD": "code",
                "NM": "name",
                "MW": "name_welsh",
            }

            return (
                {_map[k[-2:]] if k.endswith(tuple(_map.keys())) 
                else k.lower(): v for k,v in properties.items()}
            )

        for feature in data["features"]:
            properties = rename_properties(feature["properties"])
            self.geocodes[properties["code"]] = GeoCode(
                year=year,
                geometry=feature["geometry"],
                **properties)


    def load(self) -> None:
        for ref_data in self.missing_reference_data:
            data = self.download_reference_data(ref_data)
            self.create_geo_code(data, ref_data.split("_")[1])



if __name__ == "__main__":
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    geo_types = ["LAD"]
    years = ["2020"]

    a = GeoCodeLibrary(geo_types, years)
    a.load()

    for x, y in a.geocodes.items():
        print (y.code)


# def load_geocodes(self) -> None:
#         for file in self.geocode_files:
#             with fiona.open(file) as layer:
#                 for feature in layer:
#                     properties = to_dict(feature.properties)
#                     properties = rename_keys(properties)
#                     self.geocodes[properties["code"]] = GeoCode(year=years[0],geometry=feature.geometry, **properties)
