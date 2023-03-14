from django.contrib.gis import admin

from . import models


@admin.register(models.Share)
class ShareAdmin(admin.GISModelAdmin):
    list_display = ("timestamp", "location", "message")


@admin.register(models.Landscape)
class ShareAdmin(admin.GISModelAdmin):
    pass
