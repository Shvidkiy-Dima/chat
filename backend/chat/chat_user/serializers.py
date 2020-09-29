from rest_framework.serializers import ModelSerializer, ImageField
from .models import ChatUser


class ChatUserSerializer(ModelSerializer):
    image = ImageField(required=False)

    class Meta:
        model = ChatUser
        fields = ['username', 'id', 'image']