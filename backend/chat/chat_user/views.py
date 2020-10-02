from djoser.views import UserViewSet
from djoser.permissions import CurrentUserOrAdmin
from djoser.serializers import UserCreateSerializer
from .filters import UsersFilter
from .serializers import ChatUserSerializer
from core.view_mixin import ChangeSerializerMixin


class ChatUserViewSet(ChangeSerializerMixin, UserViewSet):
    filterset_class = UsersFilter
    permission_classes = [CurrentUserOrAdmin]
    serializers = {'default': ChatUserSerializer,
                   'create': UserCreateSerializer}
