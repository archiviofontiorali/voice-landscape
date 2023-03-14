from django.db.models import Max

from . import models


def calculate_places_centroid() -> list[float, float]:
    places = models.Place.objects.all()
    if not places:
        return [0, 0]
    return [
        sum(p.location.y for p in places) / len(places),
        sum(p.location.x for p in places) / len(places),
    ]


def extrapolate_place_word_frequencies() -> list[dict]:
    places = []
    for place in models.Place.objects.all():
        query = models.WordFrequency.objects.filter(place=place)
        max_frequency = query.aggregate(Max("frequency"))["frequency__max"]
        print(max_frequency)
        obj = {"coordinates": place.coordinates, "frequencies": {}}
        for wf in query.all():
            obj["frequencies"][wf.word] = wf.frequency / max_frequency
        places.append(obj)
    return places
