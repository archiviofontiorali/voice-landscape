from django.db.models import Max
from django.views import generic

from . import models


class MapContextMixin:
    @staticmethod
    def _calculate_centroid():
        places = models.Place.objects.all()
        return [
            sum(p.location.y for p in places) / len(places) if places else 0.0,
            sum(p.location.x for p in places) / len(places) if places else 0.0,
        ]

    @staticmethod
    def _fetch_place_frequencies(place: models.Place):
        query = models.WordFrequency.objects.filter(place=place)
        max_frequency = query.aggregate(Max("frequency"))["frequency__max"]

        obj = {"coordinates": place.coordinates, "frequencies": {}}
        for wf in query.all():
            obj["frequencies"][wf.word] = wf.frequency / max_frequency

        return obj

    def get_context_data(self):
        context = {
            "center": self._calculate_centroid(),
            "places": [
                self._fetch_place_frequencies(place)
                for place in models.Place.objects.all()
            ],
        }
        return context


class HomePage(generic.TemplateView):
    template_name = "home.html"


class SharePage(generic.TemplateView):
    template_name = "share.html"


class MapPage(MapContextMixin, generic.TemplateView):
    template_name = "map.html"


class ShowcasePage(MapContextMixin, generic.TemplateView):
    template_name = "showcase.html"
