from rest_framework import status
from rest_framework.decorators import action

from movie.movie_state import handle_movie_state
from streamline_be.utils import custom_response


@action(detail=False, methods=['POST'])
def add_to_watchlist(self, request, pk=None):
    movie = self.get_object()
    response = handle_movie_state(
        movie, pk, movie and movie.is_watchlisted,
        "Movie with MovieID: {movie_id} is already in watchlist",
        "add_to_watchlist"
    )
    if response:
        return response

    movie.is_watchlisted = True
    movie.save()
    return custom_response(
        data={},
        message=f"Movie with MovieID: {movie.movie_id} added to watchlist",
        code=status.HTTP_200_OK,
        endpoint=f"/api/movies/{pk}/add_to_watchlist",
        response_status=status.HTTP_200_OK
    )


@action(detail=True, methods=['POST'])
def remove_from_watchlist(self, request, pk=None):
    movie = self.get_object()
    response = handle_movie_state(
        movie, pk, not movie.is_watchlisted,
        "Movie with MovieID: {movie_id} is not in watchlist",
        "remove_from_watchlist"
    )
    if response:
        return response

    movie.is_watchlisted = False
    movie.save()
    return custom_response(
        data={},
        message=f"Movie with MovieID: {movie.movie_id} removed from watchlist",
        code=status.HTTP_200_OK,
        endpoint=f"/api/movies/{pk}/remove_from_watchlist",
        response_status=status.HTTP_200_OK
    )
