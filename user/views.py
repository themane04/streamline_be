from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from streamline_be.utils import custom_response
from .models import User
from .serializer import UserSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer, UserPasswordSerializer


class SignUpViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return custom_response(
            data=serializer.errors,
            message="Could not create user",
            code=status.HTTP_400_BAD_REQUEST,
            endpoint="/api/signup",
            response_status=status.HTTP_400_BAD_REQUEST
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class GetUserFromTokenView(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', '').split(' ')[1]
            decoded_token = AccessToken(access_token)

            user_id = decoded_token['user_id']
            user = User.objects.get(id=user_id)

            profile_image_url = (
                request.build_absolute_uri(user.profile_image.url)
                if user.profile_image
                else None
            )

            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile_image': profile_image_url,
                'date_joined': user.date_joined
            }

            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            return custom_response(
                data={},
                message=str(e),
                code=status.HTTP_400_BAD_REQUEST,
                endpoint="/api/get-user-from-token",
                response_status=status.HTTP_400_BAD_REQUEST
            )


class UpdateUserProfileView(viewsets.ViewSet):
    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                data=serializer.data,
                message="Profile updated successfully",
                code=status.HTTP_200_OK,
                endpoint=f"/api/update-profile/{user.id}",
                response_status=status.HTTP_200_OK
            )
        return custom_response(
            data=serializer.errors,
            message="Could not update profile",
            code=status.HTTP_400_BAD_REQUEST,
            endpoint=f"/api/update-profile/{user.id}",
            response_status=status.HTTP_400_BAD_REQUEST
        )


class ResetUserPasswordView(viewsets.ViewSet):
    def update(self, request, *args, **kwargs):
        serializer = UserPasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                data={},
                message="Password updated successfully",
                code=status.HTTP_200_OK,
                endpoint="/api/reset-password",
                response_status=status.HTTP_200_OK
            )
        return custom_response(
            data=serializer.errors,
            message="Could not update password",
            code=status.HTTP_400_BAD_REQUEST,
            endpoint="/api/reset-password",
            response_status=status.HTTP_400_BAD_REQUEST
        )
