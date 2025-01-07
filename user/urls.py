from rest_framework.routers import DefaultRouter

from user.views import SignUpViewSet, GetUserFromTokenView

users = DefaultRouter()
users.register('signup', SignUpViewSet, basename='signup')
users.register('get-user-from-token', GetUserFromTokenView, basename='get-user-from-token')