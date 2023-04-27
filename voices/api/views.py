from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from ..website.models import Place, WordFrequency
from .serializers import PlaceSerializer, WordFrequencySerializer


class PlaceViewSet(viewsets.ModelViewSet):
    """API endpoint for places."""

    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [permissions.IsAuthenticated]


class WordFrequencyViewSet(viewsets.ModelViewSet):
    """API endpoint for word frequencies."""

    queryset = WordFrequency.objects.all()
    serializer_class = WordFrequencySerializer
    permission_classes = [permissions.IsAuthenticated]
