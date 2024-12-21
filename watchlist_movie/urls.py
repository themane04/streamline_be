from rest_framework import routers

from watchlist_movie.views import WatchlistMovieViewSet

movies_router = routers.DefaultRouter()
movies_router.register('watchlists', WatchlistMovieViewSet, basename='watchlist_movie')