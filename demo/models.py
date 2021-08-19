import dataclasses
import pathlib
from typing import Union

Path = Union[str, pathlib.Path]


@dataclasses.dataclass
class MapOptions:
    center: [float, float]
    provider_url: str
    provider_attribution: str
