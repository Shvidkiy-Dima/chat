from channels.generic.websocket import AsyncWebsocketConsumer
from communication.utils import get_user
from asgiref.sync import sync_to_async
import json


class MessageConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # TODO: Check authorization
        user = await sync_to_async(get_user)(self.scope)
        self.group_name = str(user)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_msg(self, event):
        await self.send(json.dumps({'message': event['data']}))