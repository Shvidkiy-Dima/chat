from rest_framework.serializers import ModelSerializer, IntegerField
from django.conf import settings
from .models import Dialog, Message
from .fileds import RequestMethodField
from chat_user.serializers import ChatUserSerializer


class MessageSerializer(ModelSerializer):

    author = ChatUserSerializer(many=False, read_only=True)

    class Meta:
        model = Message
        fields = ['text', 'author', 'dialog', 'created', 'id']


class DialogSerializer(ModelSerializer):
    last_message = MessageSerializer(source='get_last_message', read_only=True)
    users = ChatUserSerializer(many=True, read_only=True)
    another_user = RequestMethodField()
    unviewed_messages = RequestMethodField()
    max_length_message = IntegerField(default=settings.MAX_LENGTH_MESSAGE)

    def get_unviewed_messages(self, dialog, request):
        return dialog.messages.exclude(who_viewed_it=request.user).count()

    def get_another_user(self, dialog, request):
        another_user = dialog.users.exclude(id=request.user.id).get()
        return ChatUserSerializer(another_user, context=self.context).data

    class Meta:
        model = Dialog
        fields = ['last_message', 'users', 'messages', 'id',
                  'another_user', 'unviewed_messages', 'max_length_message']
