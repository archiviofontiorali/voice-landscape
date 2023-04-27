from rest_framework import serializers

from ..website.models import Place, Share, WordFrequency


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
        fields = ["slug", "title", "description", "coordinates"]


class ShareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Share
        fields = ["timestamp", "coordinates", "message"]


class WordFrequencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordFrequency
        fields = ["word", "place", "frequency"]
