from django.contrib.gis.db import models


class Share(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.PointField()
    message = models.TextField(max_length=500)


class Landscape(models.Model):
    slug = models.SlugField()
    center = models.PointField()
