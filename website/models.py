import random

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db.models import Sum


class Share(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.PointField()
    message = models.TextField(max_length=500)

    @property
    def coordinates(self) -> tuple[float, float]:
        return [self.location.y, self.location.x]  # noqa


class Place(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    location = models.PointField()

    @property
    def coordinates(self) -> tuple[float, float]:
        return [self.location.y, self.location.x]  # noqa

    def __str__(self):
        if self.title:
            return self.title
        if self.slug:
            return self.slug
        if isinstance(self.location, Point):
            return f"({self.location.y:.6f}, {self.location.x:.6f})"
        return super().__str__()


class WordFrequency(models.Model):
    word = models.CharField(max_length=100)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    frequency = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = "Word Frequencies"
        constraints = [
            models.UniqueConstraint(
                fields=("word", "place"), name="WordFrequency uniqueness"
            )
        ]

    @classmethod
    def top_words(cls) -> list[tuple[str, int]]:
        query = cls.objects.values("word").annotate(total=Sum("frequency"))
        query = query.order_by("-total")[:10]
        return [(obj["word"], obj["total"]) for obj in query]

    @classmethod
    def create_random(cls):
        sample = cls(
            word=f"WORD{random.randint(0, 20):02d}",
            place=random.choice(Place.objects.all()),
            frequency=random.randint(0, 10),
        )
        if obj := cls.objects.filter(word=sample.word, place=sample.place).first():
            obj.frequency += sample.frequency
        else:
            sample.save()
