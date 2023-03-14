from django.contrib.gis.db import models


class Share(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.PointField()
    message = models.TextField(max_length=500)


class Landscape(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    center = models.PointField()


class Place(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    location = models.PointField()

    def __str__(self):
        if self.title:
            return self.title
        if self.slug:
            return self.slug
        return f"({self.location.y:.6f}, {self.location.x:.6f})"


class WordFrequency(models.Model):
    word = models.CharField(max_length=100)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    frequency = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = "Word Frequencies"
