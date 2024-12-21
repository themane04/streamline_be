from rest_framework import routers

from .views import FavoriteMovieViewSet

favorites = routers.DefaultRouter()
favorites.register('favorites', FavoriteMovieViewSet, basename='favorites')
