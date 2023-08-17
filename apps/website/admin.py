from django.conf import settings
from django.contrib import messages
from django.contrib.gis import admin
from django.utils.translation import gettext as _

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


@admin.register(models.Landscape)
class LandscapeAdmin(LocationGISModel):
    list_display = ("__str__", "title", "slug", "location")
    actions = ["set_centroid_as_location"]

    @admin.action(description="Set places' centroid as location")
    def set_centroid_as_location(self, request, queryset):
        for landscape in queryset:
            landscape.set_centroid()
            self.message_user(
                request,
                _("Set %s location to its places' centroid") % landscape,
                messages.SUCCESS,
            )
