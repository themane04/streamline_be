from rest_framework import status
from rest_framework.decorators import action

from movie.movie_state import handle_movie_state
from streamline_be.utils import custom_response


@action(detail=False, methods=['POST'])
def mark_favorite(self, request, pk=None):
    movie = self.get_object()
    response = handle_movie_state(
        movie, pk, movie and movie.is_favorite,
        "Movie with MovieID: {movie_id} is already in favorites",
        "mark_favorite"
    )
    if response:
        return response

    movie.is_favorite = True
    movie.save()
    return custom_response(
        data={},
        message=f"Movie with MovieID: {movie.movie_id} added to favorites",
        code=status.HTTP_200_OK,
        endpoint=f"/api/movies/{pk}/mark_favorite",
        response_status=status.HTTP_200_OK
    )


@action(detail=True, methods=['post'])
def unmark_favorite(self, request, pk=None):
    movie = self.get_object()
    response = handle_movie_state(
        movie, pk, not movie.is_favorite,
        "Movie with MovieID: {movie_id} is not in favorites",
        "unmark_favorite"
    )
    if response:
        return response

    movie.is_favorite = False
    movie.save()
    return custom_response(
        data={},
        message=f"Movie with MovieID: {movie.movie_id} removed from favorites",
        code=status.HTTP_200_OK,
        endpoint=f"/api/movies/{pk}/unmark_favorite",
        response_status=status.HTTP_200_OK
    )
