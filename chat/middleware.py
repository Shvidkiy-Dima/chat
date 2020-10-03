from django.utils import timezone
from .utils import Grequest


class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def before(self, request):
        pass

    def after(self, request, response):
        pass

    def __call__(self, request):
        self.before(request)
        response = self.get_response(request)
        self.after(request, response)
        return response


class UserActivityMiddleware(BaseMiddleware):

    def after(self, request, _):
        if request.user.is_authenticated:
            request.user.last_activity = timezone.now()
            request.user.save(update_fields=['last_activity'])


class GlobarRequestMiddleware(BaseMiddleware):

    def before(self, request):
        Grequest.set_request(request)
