from rest_framework.serializers import ModelSerializer
from .models import ChatUser


class ChatUserSerializer(ModelSerializer):

    class Meta:
        model = ChatUser
        fields = ['username']