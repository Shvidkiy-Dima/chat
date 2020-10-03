from django.http.request import HttpRequest
from urllib.parse import urlparse, uses_netloc

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


def parse_db_url(url, protocol='mysql'):
    uses_netloc.append(protocol)
    url = urlparse(url)
    return {'DB_NAME': url.path[1:],
            'DB_USER': url.username,
            'DB_PASSWORD': url.password,
            'DB_HOST': url.hostname,
            'DB_PORT': url.port}

Grequest = _GlobalRequest()
