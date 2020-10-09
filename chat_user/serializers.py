from django.conf import settings
from rest_framework.serializers import SerializerMethodField, ModelSerializer, ImageField
from .models import ChatUser


class ChatUserSerializer(ModelSerializer):
    is_online = SerializerMethodField()
    image = ImageField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['image'] is None:
            data['image'] = settings.DEFAULT_IMAGE

        return data

    def get_is_online(self, user):
        return user.is_online()

    class Meta:
        model = ChatUser
        fields = ['username', 'id', 'image', 'is_online']
