import math
from typing import List, Tuple

import geopy.distance

Coordinates = Tuple[float, float]


def find_nearest_place(
    target: Coordinates, places: List[Coordinates]
) -> Tuple[Coordinates, float]:
    near, distance = None, math.inf
    for place in places:
        new_distance = geopy.distance.geodesic(target, place).m
        if new_distance < distance:
            near, distance = place, new_distance
    return near, distance
