from rest_framework import viewsets, status
from rest_framework.response import Response

from streamline_be.utils import custom_response
from .models import WatchlistMovie
from .serializer import WatchlistMovieSerializer


class WatchlistMovieViewSet(viewsets.ModelViewSet):
    queryset = WatchlistMovie.objects.all()
    serializer_class = WatchlistMovieSerializer

    def create(self, request, *args, **kwargs):
        serializer = WatchlistMovieSerializer(data=request.data)
        if serializer.is_valid():
            movie_id = serializer.validated_data.get('movie_id')
            if WatchlistMovie.objects.filter(movie_id=movie_id).exists():
                return custom_response(
                    data={},
                    message=f"Movie with MovieID: {movie_id} already exists in watchlist",
                    code=status.HTTP_400_BAD_REQUEST,
                    endpoint="/api/watchlists",
                    response_status=status.HTTP_400_BAD_REQUEST
                )
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
        movies = WatchlistMovie.objects.all()
        if not movies:
            return custom_response(
                data=[],
                message="No movies found in watchlist",
                code=status.HTTP_204_NO_CONTENT,
                endpoint="/api/watchlists",
                response_status=status.HTTP_204_NO_CONTENT
            )
        serializer = WatchlistMovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            movie = WatchlistMovie.objects.get(movie_id=kwargs['pk'])
        except WatchlistMovie.DoesNotExist:
            return custom_response(
                data={},
                message=f"Movie with MovieID: {kwargs['pk']} not found in watchlist",
                code=status.HTTP_404_NOT_FOUND,
                endpoint=f"/api/watchlists/{kwargs['pk']}",
                response_status=status.HTTP_404_NOT_FOUND
            )
        serializer = WatchlistMovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            movie = WatchlistMovie.objects.get(movie_id=kwargs['pk'])
        except WatchlistMovie.DoesNotExist:
            return custom_response(
                data={},
                message=f"Movie with MovieID: {kwargs['pk']} not found in watchlist",
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
