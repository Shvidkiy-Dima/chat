from core.tests import LoginTestCase
from chat.routing import application
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from core.utils import random_string


class WSTest(LoginTestCase):
    users_count = 2

    async def _subscribe(self, conn, creds):
        token = await database_sync_to_async(self.make_token)(creds=creds)
        await conn.send_json_to({'event': 'subscribe', 'data': {'jwt': token}})

    async def _send_message(self, user, msg):
        res = await database_sync_to_async(self.client.post)('/dialog/start_dialog_with_user/',
                                                             data={'user_id': user['user'].id})

        res = await database_sync_to_async(self.client.post)(f"/dialog/{res.data['id']}/message/",
                                                             data={'text': msg,
                                                                   'dialog': res.data['id']})
        return res

    async def check_message(self, user, users_comm, another_user_comm):
        res = await self._send_message(user, random_string())
        msg_from_user, msg_from_user1 = [await comm.receive_json_from() for comm in users_comm]

        # Check that current user and user receive a new created message
        self.assertEqual(msg_from_user['data'], res.data, 'user receive wrong msg data')
        self.assertEqual(msg_from_user1['data'], res.data, 'user receive wrong msg data')

        # check that another_user didnt recieve message
        self.assertTrue(await another_user_comm.receive_nothing(), 'user receive msg')

    async def test_send_message(self):
        user1 = self.users[0]
        user2 = self.users[1]

        communicator = WebsocketCommunicator(application, "/ws/chat/")
        communicator1 = WebsocketCommunicator(application, "/ws/chat/")
        communicator2 = WebsocketCommunicator(application, "/ws/chat/")
        await communicator.connect()
        await communicator1.connect()
        await communicator2.connect()

        # Start waiting new messages in dialogs
        await self._subscribe(communicator, self.current_user_creds)
        await self._subscribe(communicator1, {'username': user1['user'].username,
                                        'password': user1['password']})

        await self._subscribe(communicator2, {'username': user2['user'].username,
                                        'password': user2['password']})

        # Start dialog with user1 and create message in that dialog
        await self.check_message(user1, (communicator, communicator1), communicator2)

        # Start dialog with user2 and create message in that dialog
        await self.check_message(user2, (communicator, communicator2), communicator1)


