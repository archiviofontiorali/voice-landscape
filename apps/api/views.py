from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from ..website.models import Place, Share, WordFrequency
from .serializers import PlaceSerializer, ShareSerializer, WordFrequencySerializer


class PlaceViewSet(viewsets.ModelViewSet):
    """API endpoint for places."""

    queryset = Place.objects.order_by("slug").all()
    serializer_class = PlaceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShareViewSet(viewsets.ModelViewSet):
    """API endpoint for shares."""

    queryset = Share.objects.order_by("timestamp").all()
    serializer_class = ShareSerializer
    permission_classes = [permissions.IsAuthenticated]


class WordFrequencyViewSet(viewsets.ModelViewSet):
    """API endpoint for word frequencies."""

    queryset = WordFrequency.objects.order_by("place", "word").all()
    serializer_class = WordFrequencySerializer
    permission_classes = [permissions.IsAuthenticated]
