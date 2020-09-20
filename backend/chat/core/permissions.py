from rest_framework.permissions import BasePermission
from .models import Dialog


class IsDialogParticipant(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user in obj.users.all()
