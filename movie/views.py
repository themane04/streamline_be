from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializer import MovieSerializer


class MovieViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        serializer = MovieSerializer()
        return Response(serializer.data)
