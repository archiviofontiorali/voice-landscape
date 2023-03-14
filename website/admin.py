from django.contrib.gis import admin

from . import models


@admin.register(models.Share)
class ShareAdmin(admin.GISModelAdmin):
    list_display = ("timestamp", "location", "message")


@admin.register(models.Place)
class PlaceAdmin(admin.GISModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("__str__", "title", "location", "description")


@admin.register(models.WordFrequency)
class WordFrequencyAdmin(admin.GISModelAdmin):
    list_display = ("word", "place", "frequency")
