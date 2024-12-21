from rest_framework import serializers

from .models import FavoriteMovie


class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = '__all__'
