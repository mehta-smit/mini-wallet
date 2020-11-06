from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import _get_error_details


class CustomException(Exception):
    status = None

    def __init__(self, message, response=None):
        self.message = message
        self.response = response

    def __str__(self):
        return _get_error_details(self.message, self.status)


class AuthenticationFailed(CustomException):
    status = status.HTTP_401_UNAUTHORIZED


def response_formatter(status_code, message, response=None):
    response_dict = dict(
        data=dict(
            status=status_code,
            message=message
        )
    )

    if response:
        response_dict['data']['response'] = response
    return Response(response_dict, status_code)


def custom_exception_handler(exc, context):
    print("Context :: {}".format(context))
    print("response ......", exc)

    return response_formatter(getattr(exc, 'status', status.HTTP_400_BAD_REQUEST), str(exc))
