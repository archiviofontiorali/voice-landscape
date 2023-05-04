from rest_framework import serializers

from ..website.models import Place, Share, WordFrequency


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "url", "slug", "title", "description", "coordinates"]


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = ["id", "url", "timestamp", "coordinates", "message"]


class WordFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = WordFrequency
        fields = ["id", "url", "word", "place", "frequency"]
