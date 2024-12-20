from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from watchlist.urls import movies_router

router = routers.SimpleRouter(trailing_slash=False)
router.registry.extend(movies_router.registry)

api_urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
]
