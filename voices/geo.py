import math
from typing import Iterable, List, Tuple

import geopy.distance

from voices.system.structures import FrequencyDict

from .models import Coordinates, Place


class PlacesDict(dict):
    def __init__(self, places: List[Coordinates]):
        super().__init__()

        for place in places:
            self.setdefault(place, FrequencyDict())

    def increment(self, place: Coordinates, key):
        self[place].increment(key)

    def increment_nearest_place(self, target: Coordinates, key):
        nearest, _distance = find_nearest_place(target, self.keys())
        self.increment(nearest, key)


def find_nearest_place(
    target: Coordinates, places: Iterable[Coordinates]
) -> Tuple[Coordinates, float]:
    near, distance = None, math.inf
    for place in places:
        new_distance = geopy.distance.geodesic(target, place).m
        if new_distance < distance:
            near, distance = place, new_distance
    return near, distance


def prepare_map_frequencies(frequency_repo) -> list:
    result = []
    for place in frequency_repo.places:
        frequencies = frequency_repo.fetch_frequency_table(place)
        max_frequency = max(frequencies.values())
        for key in frequencies:
            frequencies[key] /= max_frequency
        obj = Place(coordinates=place, frequencies=frequencies).dict()
        result.append(obj)
    return result
