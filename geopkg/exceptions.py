from dataclasses import dataclass


@dataclass
class InvalidGeoDataFrameStructure(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
