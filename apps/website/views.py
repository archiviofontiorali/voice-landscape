from django.conf import settings
from django.contrib import messages
from django.contrib.gis.geos import Point
from django.shortcuts import HttpResponse, get_object_or_404
from django.utils.translation import gettext as _
from django.views import generic

from . import forms, models


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
            messages.add_message(
                request, messages.SUCCESS, _("Grazie per la condivisione")
            )

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", forms.ShareForm())
        context.setdefault("places", models.Place.objects.all())
        return context


class LandscapeMap(generic.TemplateView):
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if slug := kwargs.pop("slug", None):
            landscape = get_object_or_404(models.Landscape, slug=slug)
        else:
            landscape = models.Landscape.objects.first()
        context["landscape"] = landscape

        centroid = landscape.centroid
        context.setdefault("center", [centroid.y, centroid.x])
        context.setdefault(
            "places",
            [
                {
                    "coordinates": place.coordinates,
                    "frequencies": place.get_frequencies(),
                }
                for place in landscape.places.all()
            ],
        )
        context.setdefault("zoom", settings.MAP_ZOOM)
        context.setdefault("provider", landscape.provider)

        return context


class LandscapeShowcase(LandscapeMap):
    template_name = "showcase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("reload", context["landscape"].reload_time)
        context.setdefault("stats", models.WordFrequency.top_words())
        return context


class PrivacyPage(generic.TemplateView):
    template_name = "privacy.html"


def robots_txt(request):
    lines = ["User-Agent: *"]
    return HttpResponse("\n".join(lines), content_type="text/plain")
