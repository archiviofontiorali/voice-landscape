from typing import List

from .geo import Coordinates, find_nearest_place
from .services import FrequencyDict


class FrequencyRepo:
    # TODO: places should be initialized by a method executed during app initialization
    # TODO: with bisect module and custom structure it's possible to improve performance
    # TODO: frequencies should be saved in an external database

    def __init__(self, service: FrequencyDict):
        self._service = service
        self._service.init_addresses([(44.6543412, 10.9011459)])

    @property
    def places(self) -> List[Coordinates]:
        return self._service.addresses

    def find_nearest_place(self, coord: Coordinates) -> Coordinates:
        return find_nearest_place(coord, self._service.addresses)[0]

    def update_frequency(self, place: Coordinates, key: str):
        self._service.increment(place, key)

    def fetch_frequency_table(self, place: Coordinates):
        return self._service.fetch_address(place)
