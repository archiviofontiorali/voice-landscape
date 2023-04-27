from rest_framework import serializers

from ..website.models import Place, WordFrequency


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
        fields = ["slug", "title", "description", "coordinates"]


class WordFrequencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordFrequency
        fields = ["word", "place", "frequency"]
