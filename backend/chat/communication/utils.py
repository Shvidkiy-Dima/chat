from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.request import HttpRequest


def get_user(scope):
    mock_request = HttpRequest()
    for header, value in scope['headers']:
        header = f'HTTP_{header.decode().upper()}'
        mock_request.META[header] = value.decode()

    user, _ = get_user_from_request(mock_request)
    return user

def get_user_from_request(request: HttpRequest):
    return JWTAuthentication().authenticate(request)