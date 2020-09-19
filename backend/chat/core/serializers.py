from rest_framework.serializers import ModelSerializer
from .models import Dialog, Message


class DialogSerializer(ModelSerializer):
    messages = ''
    class Meta:
        pass


class MessageSerializer(ModelSerializer):

    class Meta:
        pass