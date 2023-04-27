from rest_framework import serializers

from ..website.models import Place


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
        fields = ["slug", "title", "description", "coordinates"]
