from channels.generic.websocket import AsyncJsonWebsocketConsumer
from communication.utils import get_user_use_jwt
import json


class BaseMessageConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.group_name = None
        await self.accept()

    async def disconnect(self, code):
        if self.group_name is None:
            return

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        event = content['event']
        method = getattr(self, event, None)
        if method is not None:
            await method(content['data'])
        else:
            await self.send(json.dumps({'status': 'Method not exists'}))

    async def send_msg(self, event):
        await self.send(json.dumps({"type": 'message', 'data': event['data']}))


class MessageConsumer(BaseMessageConsumer):

    async def subscribe(self, data):
        token = data['jwt']
        user = await get_user_use_jwt(token)
        self.group_name = str(user)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
