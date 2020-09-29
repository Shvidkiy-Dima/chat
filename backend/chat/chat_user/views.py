from djoser.views import UserViewSet
from djoser.permissions import CurrentUserOrAdmin
from .filters import UsersFilter
from .serializers import ChatUserSerializer


class ChatUserViewSet(UserViewSet):
    filterset_class = UsersFilter
    permission_classes = [CurrentUserOrAdmin]

    def get_serializer_class(self):
        return ChatUserSerializer
