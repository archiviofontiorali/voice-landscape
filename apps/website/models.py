import random
import textwrap

from django.contrib.gis.db import models
from django.contrib.gis.db.models.aggregates import Union
from django.contrib.gis.db.models.functions import Centroid, Distance
from django.contrib.gis.geos import Point
from django.db.models import F, Max, Sum
from django.utils.translation import gettext as _

from ..geo.utils import coordinates, mercator_coordinates
from .fields import UniqueBooleanField


class TitleModel(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        if self.title:
            return self.title
        if self.slug:
            return self.slug
        return str(self.id)

    class Meta:
        abstract = True


class LocationModel(models.Model):
    location = models.PointField()

    @property
    def latitude(self) -> float:
        return self.location.y

    @property
    def longitude(self) -> float:
        return self.location.x

    @property
    def coordinates(self) -> list[float, float]:
        return coordinates(self.location)

    @property
    def mercator_coordinates(self) -> tuple[float, float]:
        return mercator_coordinates(self.latitude, self.longitude)

    def __str__(self):
        return f"({self.latitude:.4f}, {self.longitude:.4f})"

    class Meta:
        abstract = True


class Share(LocationModel):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=500)

    def __str__(self):
        message = textwrap.shorten(self.message, width=12, placeholder="...")
        return f"{super().__str__()} [{message}]"


class Place(TitleModel, LocationModel):
    description = models.TextField(max_length=500, blank=True)

    @classmethod
    def get_nearest(cls, location: Point) -> "Place":
        return (
            cls.objects.annotate(distance=Distance("location", location))
            .order_by("distance")
            .first()
        )

    def get_frequencies(self) -> list[list[str, float]]:
        """Return a list of [word, frequency] with the latest normalized"""
        max_ = self.word_frequencies.aggregate(Max("frequency"))["frequency__max"]
        return [[wf.word, wf.frequency / max_] for wf in self.word_frequencies.all()]

    def __str__(self):
        if self.title or self.slug:
            return TitleModel.__str__(self)
        return LocationModel.__str__(self)


class WordFrequency(models.Model):
    word = models.CharField(max_length=100)
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="word_frequencies",
    )
    frequency = models.PositiveIntegerField(default=0)

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
    def create_random(cls, place: Place = None):
        if place is None:
            place = random.choice(Place.objects.all())
        sample, created = cls.objects.get_or_create(
            word=f"WORD{random.randint(0, 20):02d}", place=place
        )
        sample.frequency = F("frequency") + random.randint(1, 10)
        sample.save()

    def __str__(self):
        return f"Word({self.word}, {self.frequency})"


class Landscape(TitleModel, LocationModel):
    class MapProvider(models.TextChoices):
        TONER_BACKGROUND = "Stamen.TonerBackground", _("Toner Background")
        TONER = "Stamen.Toner", _("Toner")
        TERRAIN = "Stamen.Terrain", _("Terrain")
        WATERCOLOR = "Stamen.Watercolor", _("Watercolor")

    places = models.ManyToManyField(Place, blank=True)

    reload_time = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=300,
        help_text=_("Reload time (in seconds) for showcase page"),
    )

    provider = models.CharField(
        max_length=100,
        choices=MapProvider.choices,
        default=MapProvider.TONER_BACKGROUND,
        help_text="The map provider to use with leaflet map",
    )

    default = UniqueBooleanField(default=False)

    @property
    def centroid(self) -> Point:
        if self.places.count() <= 1:
            return self.location
        return self.places.aggregate(centroid=Centroid(Union("location")))["centroid"]

    def set_centroid(self):
        self.location = self.centroid
        self.save()

    def __str__(self):
        if self.title or self.slug:
            return TitleModel.__str__(self)
        return LocationModel.__str__(self)
