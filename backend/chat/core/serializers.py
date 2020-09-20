from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Dialog, Message
from chat_user.serializers import ChatUserSerializer


class MessageSerializer(ModelSerializer):

    author = ChatUserSerializer(many=False, read_only=True)

    class Meta:
        model = Message
        fields = ['text', 'author', 'dialog']


class DialogSerializer(ModelSerializer):

    messages = SerializerMethodField()
    users = ChatUserSerializer(many=True, read_only=True)

    def get_messages(self, dialog):
        return MessageSerializer(dialog.messages.last()).data

    class Meta:
        model = Dialog
        fields = ['messages', 'users']


class DialogSerializerFull(DialogSerializer):
    messages = MessageSerializer(many=True, read_only=True)
