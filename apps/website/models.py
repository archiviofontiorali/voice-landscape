import random
import textwrap

from django.contrib.gis.db import models
from django.contrib.gis.db.models.aggregates import Union
from django.contrib.gis.db.models.functions import Centroid, Distance
from django.contrib.gis.geos import Point
from django.db.models import F, Max, Q, Sum
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from .fields import UniqueBooleanField
from .tools.geo import coordinates, mercator_coordinates


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


class TitledModel(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Share(LocationModel):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=500)
    landscape = models.ForeignKey("Landscape", on_delete=models.CASCADE)

    def __str__(self):
        message = textwrap.shorten(self.message, width=20, placeholder="...")
        return f"{super().__str__()} [{message}]"


class LeafletProvider(TitledModel):
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text=_("The short name to use with provider.js"),
    )
    url = models.URLField(
        max_length=150,
        null=True,
        blank=True,
        help_text=_("The url for a generic leaflet provider"),
    )

    def as_json(self) -> dict:
        return {"url": self.url, "name": self.name}

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(name__isnull=False) | Q(url__isnull=False),
                name="either_name_or_url_not_null",
                violation_error_message=_(
                    _("Either name or url should be set to a valid value")
                ),
            )
        ]


class Place(LocationModel):
    slug = models.SlugField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)

    description = models.TextField(max_length=500, blank=True)

    @classmethod
    def get_nearest(cls, location: Point) -> "Place":
        return (
            cls.objects.annotate(distance=Distance("location", location))
            .order_by("distance")
            .first()
        )

    def get_frequencies(self, min_frequency: int = 3) -> list[list[str, float]]:
        """Return a list of [word, frequency] with the latest normalized"""
        frequencies = self.word_frequencies.filter(
            frequency__gte=min_frequency, word__visible=True
        ).order_by("-frequency")[:50]
        max_ = frequencies.aggregate(Max("frequency"))["frequency__max"]
        return [[wf.word.text, wf.frequency / max_] for wf in frequencies]

    def as_json(self):
        return {"coordinates": self.coordinates, "frequencies": self.get_frequencies()}

    def __str__(self):
        if self.title:
            return self.title
        if self.slug:
            return self.slug
        return LocationModel.__str__(self)


class Word(models.Model):
    text = models.CharField(max_length=100, unique=True)
    visible = models.BooleanField(
        default=True,
        help_text="Set to False to hide this word in maps",
    )

    def __str__(self):
        return ("🚩 " if not self.visible else "") + self.text


class WordFrequency(models.Model):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="place_frequencies",
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="word_frequencies",
    )
    frequency = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Word Frequencies"
        ordering = ("-frequency",)
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
        return f"({self.word} | {self.place})"


class Logo(models.Model):
    name = models.CharField(max_length=150, blank=True)
    image = models.ImageField(
        upload_to="logos/", height_field="height", width_field="width"
    )
    width = models.PositiveSmallIntegerField(null=True, blank=True, editable=False)
    height = models.PositiveSmallIntegerField(null=True, blank=True, editable=False)

    @property
    def url(self):
        return self.image.url

    def __str__(self):
        return self.name if self.name else super().__str__()


class Landscape(TitledModel, LocationModel):
    description = models.TextField(max_length=500, blank=True)
    domain = models.URLField(
        blank=True,
        help_text=_("Domain in showcase page. Leave blank to use the one in .env"),
    )

    default = UniqueBooleanField(default=False)
    enabled = models.BooleanField(
        default=True,
        help_text=_("Set to False to hide it in views, unless is chosen as default"),
    )

    places = models.ManyToManyField(Place, blank=True)

    reload_time = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=300,
        help_text=_("Reload time (in seconds) for showcase page"),
    )

    provider = models.ForeignKey(
        LeafletProvider,
        on_delete=models.PROTECT,
        help_text="The map provider to use with leaflet map",
    )

    zoom_initial = models.PositiveSmallIntegerField(default=15)
    zoom_min = models.PositiveSmallIntegerField(default=13)
    zoom_max = models.PositiveSmallIntegerField(default=20)

    logo_event = models.ForeignKey(
        Logo,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None,
        related_name="+",
    )
    logo_organizer = models.ForeignKey(
        Logo,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None,
        related_name="+",
    )
    logo_partners = models.ManyToManyField(to=Logo, related_name="+", blank=True)

    @property
    def centroid(self) -> Point:
        if self.places.count() <= 1:
            return self.location
        return self.places.aggregate(centroid=Centroid(Union("location")))["centroid"]

    @property
    def zoom(self):
        return {
            "initial": self.zoom_initial,
            "min": self.zoom_min,
            "max": self.zoom_max,
        }

    def set_centroid(self):
        self.location = self.centroid
        self.save()

    @classmethod
    def get_default(cls) -> "Landscape":
        return get_object_or_404(cls, default=True)

    class VisibleLandscapeManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(Q(enabled=True) | Q(default=True))

        def get_default(self):
            return self.get(default=True)

    objects = models.Manager()
    visible_objects = VisibleLandscapeManager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="zoom_min <= zoom_initial",
                check=Q(zoom_min__lte=F("zoom_initial")),
            ),
            models.CheckConstraint(
                name="zoom_max >= zoom_initial",
                check=Q(zoom_max__gte=F("zoom_initial")),
            ),
        ]
