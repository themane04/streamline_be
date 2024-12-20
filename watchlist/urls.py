from rest_framework import routers

from watchlist.views import WatchlistViewSet

movies_router = routers.DefaultRouter()
movies_router.register('watchlists', WatchlistViewSet, basename='watchlist')