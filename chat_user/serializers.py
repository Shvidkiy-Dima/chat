from rest_framework.serializers import SerializerMethodField, ModelSerializer
from .models import ChatUser


class ChatUserSerializer(ModelSerializer):
    is_online = SerializerMethodField()

    def get_is_online(self, user):
        return user.is_online()

    class Meta:
        model = ChatUser
        fields = ['username', 'id', 'image', 'is_online']