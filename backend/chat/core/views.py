from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .permissions import IsDialogParticipant
from .models import Dialog, Message
from .serializers import DialogSerializer, MessageSerializer
from .filters import MessageFilter
from chat_user.models import UserModel


class DialogViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Dialog.objects.all()
    serializer_class = DialogSerializer
    permission_classes = [IsAuthenticated, IsDialogParticipant]

    def get_queryset(self):
        return self.request.user.get_my_dialogs()

    @action(detail=False, methods=['post'])
    def start_dialog_with_user(self, request):

        # TODO: Will need to delete Dialogs that dont have msgs during several weeks

        another_user = UserModel.objects.get(id=request.data['user_id'])
        dialog = Dialog.objects.get_or_create_dialog(request.user, another_user)
        dialog = DialogSerializer(dialog)
        return Response(dialog.data)


def MsgPermCallback(req, view):
    dialog_id = view.kwargs['dialog']
    dialog = Dialog.objects.get(id=dialog_id)
    return req.user in dialog.users.all()


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    filterset_class = MessageFilter
    permission_classes = [IsAuthenticated,
                          IsDialogParticipant(callback=MsgPermCallback)]

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        for m in qs.exclude(who_viewed_it=self.request.user).iterator():
            m.who_viewed_it.add(self.request.user)

        return qs

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

