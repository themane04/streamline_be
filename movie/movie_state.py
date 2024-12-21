from rest_framework import status

from streamline_be.utils import custom_response


def handle_movie_state(movie, pk, state_check, state_message, endpoint_suffix):
    if not movie:
        return custom_response(
            data={},
            message=f"Movie with MovieID: {pk} not found",
            code=status.HTTP_404_NOT_FOUND,
            endpoint=f"/api/movies/{pk}",
            response_status=status.HTTP_404_NOT_FOUND
        )
    elif state_check:
        return custom_response(
            data={},
            message=state_message.format(movie_id=movie.movie_id),
            code=status.HTTP_400_BAD_REQUEST,
            endpoint=f"/api/movies/{pk}/{endpoint_suffix}",
            response_status=status.HTTP_400_BAD_REQUEST
        )
    return None
