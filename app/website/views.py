import datetime as dt
import random
from collections import Counter, defaultdict
from typing import Iterable, Optional

from django.conf import settings
from django.contrib import messages
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Min, Q
from django.shortcuts import get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from . import forms, models


class LandscapeTemplateView(TemplateView):
    def get_landscape(self) -> models.Landscape:
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
    def get_context_data(self, slug: Optional[str] = None, **kwargs):
        context = super().get_context_data(**kwargs)

        landscape: models.Landscape = context["landscape"]

        map_ = get_object_or_404(
            landscape.maps, Q(slug=slug) if slug else Q(default=True)
        )

        context["map"] = map_
        context["maps"] = landscape.maps.all()

        context.setdefault("overlay", map_.overlay)
        context.setdefault("center", map_.centroid)
        context.setdefault("zoom", map_.zoom)

        context.setdefault("use_simple_crs", not settings.VOICES_ENABLE_GEODJANGO)

        context.setdefault(
            "provider", landscape.provider.as_json() if landscape.provider else None
        )
        context.setdefault("places", [place.as_json() for place in map_.places.all()])

        return context


class Map(MapTemplateView):
    template_name = "website/map.html"


class Share(LandscapeTemplateView):
    template_name = "website/share.html"
    phrases = [
        _("Rendi la tua voce parte dell'esperienza che stai vivendo adesso."),
        _("Quale frase emerge nella tua mente attraversando questo spazio?"),
        _("A cosa stai pensando?"),
        _("Fermati... respira... Cosa vedi di fronte a te?"),
        _("Parole... Parole... Parole..."),
        _("Raccogli l'essenza dell'attimo presente in una frase..."),
    ]

    def post(self, request, slug: Optional[str] = None):
        form = forms.ShareForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data["message"]

            latitude = float(form.cleaned_data["latitude"])
            longitude = float(form.cleaned_data["longitude"])
            slug = form.cleaned_data.get("place")

            if not slug:
                location = Point(x=longitude, y=latitude)
                place_ = models.Place.get_nearest(location)
            else:
                place_ = models.Place.objects.get(slug=slug)

            share = models.Share(
                message=message, place=place_, landscape=self.get_landscape()
            )
            if settings.VOICES_ENABLE_GEODJANGO:
                share.location = Point(x=longitude, y=latitude)
            else:
                share.x, share.y = longitude, latitude

            share.save()

            messages.success(request, _("Grazie per la condivisione"))

            map_ = place_.maps.filter(landscape__pk=self.get_landscape().pk).first()
            # map_ = place_.maps.first()
            url = resolve_url("website:map", slug=map_.slug if map_ else None)
            return redirect(url)

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, slug: Optional[str] = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("phrase", random.choice(self.phrases))
        context.setdefault("form", forms.ShareForm())

        context.setdefault("places", places := context["landscape"].places.all())
        context.setdefault("selected", places.filter(slug=slug).first())

        context.setdefault("enable_sharing", settings.VOICES_ENABLE_SHARING)
        context.setdefault("enable_gps", settings.VOICES_ENABLE_GPS)

        return context


class HistoryMap(MapTemplateView):
    template_name = "website/history.html"

    def get_context_data(self, slug: Optional[str] = None, **kwargs):
        context = super().get_context_data(slug=slug, **kwargs)

        timestamp = kwargs.get("timestamp", timezone.now())
        timestamp_range = models.Share.objects.aggregate(
            min=Min("timestamp"), max=Max("timestamp")
        )
        timestamp_min = timestamp_range["min"].date()
        timestamp_max = timestamp_range["max"].date()
        if timestamp.date() > timestamp_max:
            timestamp = dt.datetime.combine(timestamp_max, dt.time(23, 00))

        context["timestamp"] = {
            "current": timestamp,
            "first_date": timestamp_min,
            "last_date": timestamp_max,
        }
        context["date_range"] = list(date_range(timestamp_min, timestamp_max))
        context["time_range"] = [dt.time(h, 0) for h in range(24)]

        counters = defaultdict[models.Place | None, Counter[models.Word]](
            lambda: Counter()
        )

        timestamp_limit = timestamp + dt.timedelta(hours=1)
        for share in models.Share.objects.filter(timestamp__lt=timestamp_limit):
            for word in share.words.all():
                counters[share.place][word] += 1

        output = []
        for place, counter in counters.items():
            if not counter:
                continue
            max_value = max(counter.values())
            frequencies = [
                [word.text, count / max_value] for word, count in counter.items()
            ]
            output.append(
                {
                    "coordinates": place.coordinates if place else None,
                    "frequencies": frequencies,
                }
            )

        context["places"] = output

        return context


def date_range(first_date: dt.date, last_date: dt.date) -> Iterable[dt.date]:
    date = first_date
    while date <= last_date:
        yield date
        date += dt.timedelta(days=1)


def qr_code_redirect(request, slug: str):
    return redirect("website:share", slug=slug)
