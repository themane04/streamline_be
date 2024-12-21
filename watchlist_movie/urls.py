from rest_framework import routers

from .views import WatchlistMovieViewSet

watchlists = routers.DefaultRouter()
watchlists.register('watchlists', WatchlistMovieViewSet, basename='watchlists')