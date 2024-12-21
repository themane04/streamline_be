from rest_framework import serializers

from watchlist_movie.models import WatchlistMovie


class WatchlistMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchlistMovie
        fields = '__all__'