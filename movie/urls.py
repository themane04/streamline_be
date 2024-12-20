from rest_framework import routers

from movie.views import MovieViewSet

movies_router = routers.DefaultRouter()
movies_router.register('movies', MovieViewSet, basename='movies')