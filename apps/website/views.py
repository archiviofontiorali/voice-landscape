from django.contrib import messages
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from . import forms, models


class LandscapeTemplateView(TemplateView):
    def get_landscape(self):
        try:
            slug = self.request.COOKIES.get("landscape")
            return models.Landscape.visible_objects.get(slug=slug)
        except ObjectDoesNotExist:
            return get_object_or_404(models.Landscape.visible_objects, default=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["landscape"] = self.get_landscape()
        context["landscapes"] = models.Landscape.visible_objects.values_list(
            "slug", "title"
        )
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie(
            "landscape", context["landscape"].slug, path="/", samesite="Lax"
        )
        return response


class MapTemplateView(LandscapeTemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        landscape: models.Landscape = context["landscape"]
        centroid = landscape.centroid

        context.setdefault("center", [centroid.y, centroid.x])
        context.setdefault("zoom", landscape.zoom)
        context.setdefault("provider", landscape.provider.as_json())
        context.setdefault(
            "places", [place.as_json() for place in context["landscape"].places.all()]
        )

        return context


class Share(LandscapeTemplateView):
    template_name = "website/share.html"

    def post(self, request):
        form = forms.ShareForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data["message"]

            latitude = float(form.cleaned_data["latitude"])
            longitude = float(form.cleaned_data["longitude"])
            location = Point(x=longitude, y=latitude)

            landscape = self.get_landscape()

            share = models.Share(
                message=message, location=location, landscape=landscape
            )
            share.save()
            messages.success(request, _("Grazie per la condivisione"))
            return redirect("website:map")

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", forms.ShareForm())
        context.setdefault("places", context["landscape"].places.all())
        return context


class Map(MapTemplateView):
    template_name = "website/map.html"
