from django.contrib.gis import admin

from . import models


@admin.register(models.Share)
class ShareAdmin(admin.GISModelAdmin):
    list_display = ("timestamp", "location", "message")


@admin.register(models.Landscape)
class LandscapeAdmin(admin.GISModelAdmin):
    list_display = ("title", "center")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(models.Place)
class PlaceAdmin(admin.GISModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    def location(self):
        return f"({self.location.y:.6f}, {self.location.x:.6f})"

    list_display = ("title", "location", "description")


@admin.register(models.WordFrequency)
class WordFrequencyAdmin(admin.GISModelAdmin):
    list_display = ("word", "place", "frequency")
