from django.http.request import HttpRequest


class _GlobalRequest:

    def __init__(self):
        self.request = None

    def set_request(self, request: HttpRequest):
        self.request = request

    def __getattr__(self, item):
        if self.request is None:
            raise RuntimeError('Request must be HttpRequest instance or maybe you'
                               'forgot set GlobarRequestMiddleware')

        return getattr(self.request, item)


Grequest = _GlobalRequest()
