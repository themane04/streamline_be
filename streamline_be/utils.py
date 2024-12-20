from rest_framework.response import Response
from rest_framework import status


def custom_response(data=None, message="", code=None, endpoint="", response_status=status.HTTP_200_OK):
    response_data = {
        "code": code if code is not None else response_status,
        "message": message,
        "endpoint": endpoint,
        "data": data
    }
    return Response(response_data, status=response_status)
