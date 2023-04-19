from django.conf import settings
from django.contrib.gis.geos import Point
from django.db.models import Max
from django.views import generic

from . import forms, models


class MapContextMixin:
    @staticmethod
    def _calculate_centroid():
        places = models.Place.objects.values("location")
        return [
            sum(p["location"].y for p in places) / len(places) if places else 0.0,
            sum(p["location"].x for p in places) / len(places) if places else 0.0,
        ]

    @staticmethod
    def _fetch_place_frequencies(place: models.Place):
        max_frequency = place.word_frequencies.aggregate(Max("frequency"))[
            "frequency__max"
        ]

        return {
            "coordinates": place.coordinates,
            "frequencies": [
                [wf.word, wf.frequency / max_frequency]
                for wf in place.word_frequencies.all()
            ],
        }

    def get_context_data(self):
        context: dict = {
            "center": self._calculate_centroid(),
            "places": [
                self._fetch_place_frequencies(place)
                for place in models.Place.objects.all()
            ],
            "zoom": settings.LANDSCAPE_DEFAULT_ZOOM,
            "provider": settings.LANDSCAPE_PROVIDER,
        }
        return context


class HomePage(generic.TemplateView):
    template_name = "home.html"


class SharePage(generic.TemplateView):
    template_name = "share.html"

    def post(self, request):
        form = forms.ShareForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data["message"]

            latitude = float(form.cleaned_data["latitude"])
            longitude = float(form.cleaned_data["longitude"])
            location = Point(x=longitude, y=latitude)

            share = models.Share(message=message, location=location)
            share.save()

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", forms.ShareForm())
        context.setdefault("places", models.Place.objects.all())
        return context


class MapPage(MapContextMixin, generic.TemplateView):
    template_name = "map.html"


class ShowcasePage(MapContextMixin, generic.TemplateView):
    template_name = "showcase.html"

    def get_context_data(self):
        context = super().get_context_data()
        context.setdefault("reload", 5 * 60)
        context.setdefault("stats", models.WordFrequency.top_words())
        return context


class PrivacyPage(generic.TemplateView):
    template_name = "privacy.html"
