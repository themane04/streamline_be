from rest_framework.routers import DefaultRouter

from user.views import SignUpViewSet, GetUserFromTokenView, UpdateUserProfileView, ResetUserPasswordView

users = DefaultRouter()
users.register('signup', SignUpViewSet, basename='signup')
users.register('get-user-from-token', GetUserFromTokenView, basename='get-user-from-token')
users.register('update-profile', UpdateUserProfileView, basename='update-profile')
users.register('reset-password', ResetUserPasswordView, basename='reset-password')