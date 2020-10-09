from rest_framework.permissions import BasePermissionMetaclass
from functools import partial


class BaseDinamicPermissionMetaclass(BasePermissionMetaclass):

    def __call__(cls, callback=None):
        call = super().__call__
        return partial(call, callback) if callback else super().__call__(callback)


class BaseDinamicPermission(metaclass=BaseDinamicPermissionMetaclass):

    def __init__(self, callback):
        self.callback = callback

    def has_permission(self, request, view):
        return self.callback(request, view) if self.callback else True
