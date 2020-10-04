from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from string import ascii_letters
from hashlib import md5
from functools import wraps
import random


def random_string(length=10):
    return ''.join(random.choices(ascii_letters, k=length))


def get_uniq_key(req):
    key = req.path + req.user.username + str(req.data) + str(req.query_params)
    hash_ = md5(key.encode())
    return hash_.hexdigest()


def cached(sec):

    def _cached(f):

        @wraps(f)
        def _inner_cached(self, req, *args, **kwargs):
            key = get_uniq_key(req)
            res_data = cache.get(key)
            if res_data is None:
                response = f(self, req, *args, **kwargs)
                res_data = {'data': response.data,
                            'status': response.status_code,
                            'headers': dict(response.items()),
                            'content_type': response.content_type}

                if status.is_success(response.status_code):
                    cache.add(key, res_data, sec)

            return Response(**res_data)

        return _inner_cached

    return _cached
