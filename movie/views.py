from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from streamline_be.utils import custom_response
from .favorites import mark_favorite as fav_mark, unmark_favorite as fav_unmark
from .watchlist import add_to_watchlist as watch_add, remove_from_watchlist as watch_remove
from .models import Movie
from .serializer import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    mark_favorite = action(detail=True, methods=['POST'])(fav_mark)
    unmark_favorite = action(detail=True, methods=['POST'])(fav_unmark)
    add_to_watchlist = action(detail=True, methods=['POST'])(watch_add)
    remove_from_watchlist = action(detail=True, methods=['POST'])(watch_remove)

    def get_object(self):
        movie_id = self.kwargs.get('pk')
        return get_object_or_404(Movie, movie_id=movie_id)

    def create(self, request, *args, **kwargs):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            movie_id = serializer.validated_data.get('movie_id')
            if Movie.objects.filter(movie_id=movie_id).exists():
                return custom_response(
                    data={},
                    message=f"Movie with MovieID: {movie_id} already exists in movie",
                    code=status.HTTP_400_BAD_REQUEST,
                    endpoint="/api/movies",
                    response_status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return custom_response(
                data=serializer.data,
                message="Movie added successfully",
                code=status.HTTP_201_CREATED,
                endpoint="/api/movies",
                response_status=status.HTTP_201_CREATED
            )
        return custom_response(
            data=serializer.errors,
            message="Could not add movie to movies",
            code=status.HTTP_400_BAD_REQUEST,
            endpoint="/api/movies",
            response_status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request, *args, **kwargs):
        if 'favorites' in request.query_params:
            movies = Movie.objects.filter(is_favorite=True)
        elif 'watchlist' in request.query_params:
            movies = Movie.objects.filter(is_watchlisted=True)
        else:
            movies = Movie.objects.all()
        if not movies:
            return custom_response(
                data=[],
                message="No movies found",
                code=status.HTTP_204_NO_CONTENT,
                endpoint="/api/movies",
                response_status=status.HTTP_204_NO_CONTENT
            )
        serializer = MovieSerializer(movies, many=True)
        return custom_response(
            data=serializer.data,
            message="Movies retrieved successfully",
            code=status.HTTP_200_OK,
            endpoint="/api/movies",
            response_status=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(movie_id=kwargs['pk'])
        except Movie.DoesNotExist:
            return custom_response(
                data={},
                message=f"Movie with MovieID: {kwargs['pk']} not found",
                code=status.HTTP_404_NOT_FOUND,
                endpoint=f"/api/movies/{kwargs['pk']}",
                response_status=status.HTTP_404_NOT_FOUND
            )
        serializer = MovieSerializer(movie)
        return custom_response(
            data=serializer.data,
            message=f"Movie with MovieID: {kwargs['pk']} retrieved successfully",
            code=status.HTTP_200_OK,
            endpoint=f"/api/movies/{kwargs['pk']}",
            response_status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(movie_id=kwargs['pk'])
        except Movie.DoesNotExist:
            return custom_response(
                data={},
                message=f"Movie with MovieID: {kwargs['pk']} not found",
                code=status.HTTP_404_NOT_FOUND,
                endpoint=f"/api/movies/{kwargs['pk']}",
                response_status=status.HTTP_404_NOT_FOUND
            )
        movie.delete()
        return custom_response(
            data={},
            message=f"Movie with MovieID: {kwargs['pk']} deleted successfully",
            code=status.HTTP_204_NO_CONTENT,
            endpoint="/api/movies",
            response_status=status.HTTP_204_NO_CONTENT
        )
