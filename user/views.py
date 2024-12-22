from rest_framework import viewsets, status
from rest_framework_simplejwt.views import TokenObtainPairView

from streamline_be.utils import custom_response
from .serializer import UserSerializer, CustomTokenObtainPairSerializer


class SignUpViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                data=serializer.data,
                message="User created successfully",
                code=status.HTTP_201_CREATED,
                endpoint="/api/signup",
                response_status=status.HTTP_201_CREATED
            )
        return custom_response(
            data=serializer.errors,
            message="Could not create user",
            code=status.HTTP_400_BAD_REQUEST,
            endpoint="/api/signup",
            response_status=status.HTTP_400_BAD_REQUEST
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
