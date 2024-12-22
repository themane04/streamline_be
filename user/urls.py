from rest_framework.routers import DefaultRouter

from user.views import SignUpViewSet

users = DefaultRouter()
users.register('signup', SignUpViewSet, basename='signup')