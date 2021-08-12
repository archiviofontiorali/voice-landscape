import dataclasses


@dataclasses.dataclass
class MapOptions:
    center: [float, float]
    provider_url: str
    provider_attribution: str
