from django.contrib.gis.db import models


class Share(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.PointField()
    message = models.TextField(max_length=500)


class Landscape(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    center = models.PointField()
