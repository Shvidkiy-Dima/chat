from rest_framework.serializers import ImageField, SerializerMethodField
from djoser.serializers import UserCreateSerializer
from .models import ChatUser


class ChatUserSerializer(UserCreateSerializer):
    image = ImageField(required=False)
    is_online = SerializerMethodField()

    def get_is_online(self, user):
        return user.is_online()

    class Meta:
        model = ChatUser
        fields = ['username', 'id', 'image', 'password', 'is_online']