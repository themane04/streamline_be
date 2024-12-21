from rest_framework import routers

from .views import MovieViewSet

movies = routers.DefaultRouter()
movies.register('movies', MovieViewSet, basename='movies')