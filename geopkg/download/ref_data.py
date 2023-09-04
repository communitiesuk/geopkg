
import requests
from dataclasses import dataclass

@dataclass
class RefData:
    filename: str

    def download(self) -> dict:
        url = (
            "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
            f"{self.filename} /FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=geojson"
        )

        ret_data = requests.get(url)
        return ret_data.json()


reference_config: dict[str, dict[str, str]] = {
  "LAD": {
    "2023": {
      "filename": "Local_Authority_Districts_May_2023_UK_BFC_V2"
    },
    "2022": {
      "filename": "Local_Authority_Districts_May_2022_UK_BFC_V3_2022"
    },
    "2021": {
      "filename": "Local_Authority_Districts_May_2021_UK_BFC_2022"
    },
    "2020": {
      "filename": "LAD_Dec_2020_UK_BFC_2022"
    },
    "2019": {
      "filename": "Local_Authority_Districts_April_2019_UK_BFC_2022"
    },
    "2018": {
      "filename": "LAD_Dec_2018_Boundaries_GB_BFC_2022"
    },
    "2017": {
      "filename": "Local_Authority_Districts_December_2017_Boundaries_GB_BFC_2022"
    },
    "2016": {
      "filename": "Local_Authority_Districts_December_2016_GB_BFC_2022"
    },
    "2015": {
      "filename": "LAD_Dec_2015_FCB_GB_2022"
    },
    "2014": {
      "filename": "LAD_DEC_2014_GB_BFC"
    },
    "2013": {
      "filename": "LAD_DEC_2013_GB_BFC"
    },
    "2012": {
      "filename": "LAD_DEC_2012_GB_BFC"
    },
    "2011": {
      "filename": "Local_Authority_Districts_December_2011_GB_BFC_2022"
    },
    "2009": {
      "filename": "LAD_Dec_2009_FCB_in_Great_Britain_2022"
    }
  }
}
