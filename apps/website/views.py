from django.contrib import messages
from django.contrib.gis.geos import Point
from django.shortcuts import HttpResponse, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.views import generic

from . import forms, models


class LandscapeTemplateView(generic.TemplateView):
    @staticmethod
    def get_landscape(slug: str = None):
        query = dict(slug=slug) if slug else dict(default=True)
        return get_object_or_404(models.Landscape, **query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = context.setdefault("slug", None)
        context["landscape"] = self.get_landscape(slug)

        return context


class LandscapeMapPage(LandscapeTemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        landscape = context["landscape"]
        centroid = landscape.centroid

        context.setdefault("center", [centroid.y, centroid.x])
        context.setdefault("zoom", landscape.zoom)
        context.setdefault(
            "provider",
            {
                "url": landscape.provider.url,
                "name": landscape.provider.name,
            },
        )

        return context


class SharePage(LandscapeTemplateView):
    template_name = "share.html"

    def post(self, request, slug: str = None):
        form = forms.ShareForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data["message"]

            latitude = float(form.cleaned_data["latitude"])
            longitude = float(form.cleaned_data["longitude"])
            location = Point(x=longitude, y=latitude)

            landscape = self.get_landscape(slug)

            share = models.Share(
                message=message, location=location, landscape=landscape
            )
            share.save()
            messages.success(request, _("Grazie per la condivisione"))
            return redirect("map", slug=landscape.slug)

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", forms.ShareForm())
        context.setdefault("places", context["landscape"].places.all())
        return context


class MapPage(LandscapeMapPage):
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        landscape = context["landscape"]
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
        return context


def robots_txt(request):
    lines = ["User-Agent: *"]
    return HttpResponse("\n".join(lines), content_type="text/plain")
