from django.conf import settings
from django.contrib import messages
from django.contrib.gis import admin
from django.utils.translation import gettext as _

from . import models


class LocationGISModel(admin.GISModelAdmin):
    list_display = ("location",) if settings.VOICES_ENABLE_GEODJANGO else ("x", "y")
    # gis_widget = OSMWidget|OpenLayersWidget
    gis_widget_kwargs = {
        "attrs": {
            "default_zoom": 11,
            "default_lon": settings.DEFAULT_POINT.y,
            "default_lat": settings.DEFAULT_POINT.x,
        },
    }


@admin.register(models.LeafletProvider)
class LeafletProviderAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("__str__", "title", "slug", "name", "url")


@admin.register(models.Share)
class ShareAdmin(LocationGISModel):
    list_display = ("timestamp", "message", "place", *LocationGISModel.list_display)


@admin.register(models.Place)
class PlaceAdmin(LocationGISModel):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "title",
        *LocationGISModel.list_display,
        "id",
        "slug",
        "description",
    )
    ordering = ["title"]


class WordFrequencyInline(admin.TabularInline):
    model = models.WordFrequency
    extra = 1


@admin.register(models.WordFrequency)
class WordFrequencyAdmin(admin.GISModelAdmin):
    list_display = ("word", "place", "frequency")


@admin.register(models.Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("text", "visible")
    inlines = [WordFrequencyInline]


@admin.register(models.Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "width", "height")


@admin.register(models.Landscape)
class LandscapeAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "__str__",
        "title",
        "slug",
        "domain",
        "default",
        "provider",
    )


@admin.register(models.Map)
class MapAdmin(LocationGISModel):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "__str__",
        "title",
        "slug",
        *LocationGISModel.list_display,
        "default",
        "enabled",
    )
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
