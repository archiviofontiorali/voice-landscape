from typing import List

from .geo import Coordinates, find_nearest_place


class FrequencyRepo:
    # TODO: places should be initialized by a method executed during app initialization
    # TODO: with bisect module and custom structure it's possible to improve performance
    # TODO: frequencies should be saved in an external database

    def __init__(self):
        self._places = [(44.6543412, 10.9011459)]
        self._frequencies = {coord: dict(test=1) for coord in self._places}

    @property
    def places(self) -> List[Coordinates]:
        return self._places

    def find_nearest_place(self, coord: Coordinates) -> Coordinates:
        return find_nearest_place(coord, self._places)[0]

    def update_frequency(self, place: Coordinates, key: str):
        frequency_table = self._frequencies[place]
        try:
            frequency_table[key] += 1
        except KeyError:
            frequency_table[key] = 1

    def fetch_frequency_table(self, place: Coordinates):
        return self._frequencies[place]
