from rest_framework import viewsets, status
from rest_framework.response import Response

from streamline_be.utils import custom_response
from .models import Watchlist
from .serializer import WatchlistSerializer


class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer

    def create(self, request, *args, **kwargs):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return custom_response(
            data=serializer.errors,
            message="Could not add movie to watchlist",
            code=status.HTTP_400_BAD_REQUEST,
            endpoint="/api/watchlists",
            response_status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request, *args, **kwargs):
        movies = Watchlist.objects.all()
        if not movies:
            return custom_response(
                data=[],
                message="No movies found in watchlist",
                code=status.HTTP_204_NO_CONTENT,
                endpoint="/api/watchlists",
                response_status=status.HTTP_204_NO_CONTENT
            )
        serializer = WatchlistSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            movie = Watchlist.objects.get(movie_id=kwargs['pk'])
        except Watchlist.DoesNotExist:
            return custom_response(
                data={},
                message=f"Movie with MovieID: {kwargs['pk']} not found in watchlist",
                code=status.HTTP_404_NOT_FOUND,
                endpoint=f"/api/watchlists/{kwargs['pk']}",
                response_status=status.HTTP_404_NOT_FOUND
            )
        serializer = WatchlistSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            movie = Watchlist.objects.get(movie_id=kwargs['pk'])
        except Watchlist.DoesNotExist:
            return custom_response(
                data={},
                message=f"Movie with ID: {kwargs['pk']} not found in watchlist",
                code=status.HTTP_404_NOT_FOUND,
                endpoint=f"/api/watchlists/{kwargs['pk']}",
                response_status=status.HTTP_404_NOT_FOUND
            )
        movie.delete()
        return custom_response(
            data={},
            message="Movie deleted successfully from watchlist",
            code=status.HTTP_204_NO_CONTENT,
            endpoint="/api/watchlists",
            response_status=status.HTTP_204_NO_CONTENT
        )
