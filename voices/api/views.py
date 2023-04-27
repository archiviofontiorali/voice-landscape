from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from ..website.models import Place
from .serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    """API endpoint for places."""

    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [permissions.IsAuthenticated]
