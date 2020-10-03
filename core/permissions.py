from .permission_mixin import BaseDinamicPermission


class IsDialogParticipant(BaseDinamicPermission):

    def has_object_permission(self, request, view, obj):
        return request.user in obj.users.all()
