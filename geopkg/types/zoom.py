from typing import Literal

SupportedZoomLevels = Literal[
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18
]

MAX_ZOOM = 18


class Zoom:
    def __getitem__(self, index: SupportedZoomLevels) -> int:
        if index not in range(1, MAX_ZOOM + 1):
            raise IndexError(f"Zoom level {index} is not supported")
        return index
