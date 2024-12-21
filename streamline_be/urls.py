from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from favorite_movies.urls import favorites
from watchlist_movie.urls import watchlists

router = routers.SimpleRouter(trailing_slash=False)
router.registry.extend(watchlists.registry)
router.registry.extend(favorites.registry)

api_urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
]
