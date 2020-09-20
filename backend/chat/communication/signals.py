from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Message
from core.serializers import MessageSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver(post_save, sender=Message, dispatch_uid='create_msg')
def message_handler(sender, instance, **kwargs):
    layer = get_channel_layer()
    data = MessageSerializer(instance).data
    for user in instance.dialog.users.all():
        group_name = str(user)
        async_to_sync(layer.group_send)(group_name, {'type': 'send_msg', 'data': data })
