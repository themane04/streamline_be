from rest_framework import serializers

from .models import WatchlistMovie


class WatchlistMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchlistMovie
        fields = '__all__'