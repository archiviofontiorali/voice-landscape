from django.conf import settings
from django.contrib.gis import admin

from . import models


class LocationGISModel(admin.GISModelAdmin):
    gis_widget_kwargs = {
        "attrs": {
            "default_zoom": 11,
            "default_lon": settings.DEFAULT_POINT_LONGITUDE,
            "default_lat": settings.DEFAULT_POINT_LATITUDE,
        },
    }


@admin.register(models.Share)
class ShareAdmin(LocationGISModel):
    list_display = ("timestamp", "location", "message")


@admin.register(models.Place)
class PlaceAdmin(LocationGISModel):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("__str__", "title", "location", "description")


@admin.register(models.WordFrequency)
class WordFrequencyAdmin(admin.GISModelAdmin):
    list_display = ("word", "place", "frequency")
