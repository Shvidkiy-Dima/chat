from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.request import HttpRequest
from asgiref.sync import sync_to_async


async def get_user_use_jwt(jwt):
    request = get_request_use_jwt(jwt)
    user, _ = await sync_to_async(get_user_from_request)(request)
    return user


def get_request_use_jwt(jwt):
    mock_request = HttpRequest()
    header = 'HTTP_AUTHORIZATION'
    mock_request.META[header] = jwt
    return mock_request


def get_user_from_request(request: HttpRequest):
    return JWTAuthentication().authenticate(request)
