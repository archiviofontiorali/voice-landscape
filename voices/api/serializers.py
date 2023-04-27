from rest_framework import serializers

from ..website.models import Place, Share, WordFrequency


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
        fields = ["url", "slug", "title", "description", "coordinates"]


class ShareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Share
        fields = ["url", "timestamp", "coordinates", "message"]


class WordFrequencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordFrequency
        fields = ["url", "word", "place", "frequency"]
