import pathlib

from pydantic import BaseModel

Path = pathlib.Path | str
Coordinates = tuple[float, float]


class Place(BaseModel):
    coordinates: Coordinates
    frequencies: dict[str, float]
