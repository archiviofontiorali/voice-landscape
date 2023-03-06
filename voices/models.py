import pathlib
from dataclasses import dataclass
from typing import Dict, Tuple, Union

from dataclasses_json import dataclass_json

Path = Union[str, pathlib.Path]
Coordinates = Tuple[float, float]


@dataclass_json
@dataclass
class Place:
    coordinates: Coordinates
    frequencies: Dict[str, float]
