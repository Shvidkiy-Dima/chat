from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .permissions import IsDialogParticipant
from .models import Dialog, Message
from .serializers import DialogSerializer, DialogSerializerFull, MessageSerializer
from django.contrib.auth import get_user_model

class DialogViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Dialog.objects.all()
    serializer_class = DialogSerializer
    # permission_classes = [IsAuthenticated, IsDialogParticipant]

    # def get_queryset(self):
    #     return self.request.user.dialogs.all()

    @action(detail=False, methods=['get'])
    def get_dialog_with_user(self, request):
        another_user = get_user_model().objects.get(id=request.query_params['another_user_id'])
        dialog = Dialog.objects.filter(users__in=[request.user]).filter(users__in=[another_user])
        if not dialog:
            return Response({'status': 'new'})

        dialog = DialogSerializer(dialog.first())
        return Response(dialog.data)

    @action(detail=False, methods=['post'])
    def initialize_dialog(self, request):
        another_user_id = request.data['another_user_id']
        another_user = get_user_model().objects.get(id=another_user_id)
        user = request.user

        if Dialog.objects.filter(users__in=[request.user]).filter(users__in=[another_user]).exists():
            return Response({'err': 'd exists'}, status=status.HTTP_400_BAD_REQUEST)

        dialog = Dialog.objects.create()
        dialog.users.add(user)
        dialog.users.add(another_user)

        data = {'dialog': dialog,
                'author': user,
                'text': request.data.get('text')
                }
        res = self._create_message(data)
        if not status.is_success(res.status_code):
            dialog.delete()

        return res

    @action(detail=False, methods=['post'])
    def create_message(self, request):
        data = {'dialog': self.get_object(),
                'author': request.user,
                'text': request.data.get('text')
                }
        return self._create_message(data)

    def _create_message(self, data):
        message = MessageSerializer(data=data)
        if message.is_valid():
            message.save()
            return Response(message.data, status=status.HTTP_201_CREATED)

        return Response(message.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        return DialogSerializerFull if self.detail else DialogSerializer
