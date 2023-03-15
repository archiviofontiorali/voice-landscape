import math
from typing import Iterable, Tuple

import geopy.distance

from .models import Coordinates, Place


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
