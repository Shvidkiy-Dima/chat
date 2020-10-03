from rest_framework.test import APITestCase
from rest_framework import status
from chat_user.models import UserModel
from core.models import Dialog, Message
from core.utils import random_string
from core.serializers import MessageSerializer
from itertools import takewhile

class LoginTestCase(APITestCase):
    users_count = 2
    need_to_login = True
    current_user_creds = {}

    @classmethod
    def _create_user(cls, username, password):
        u = UserModel.objects.create(username=username)
        u.set_password(password)
        u.save()
        return {'user': u, 'password': password}

    @classmethod
    def setUpClass(cls):
        username, password = random_string(), random_string()
        cls.current_user_creds = {'username': username, 'password': password}
        cls.current_user = cls._create_user(username, password)['user']
        cls.users = [cls._create_user(random_string(), random_string())
                     for _ in range(cls.users_count)]
        return super().setUpClass()

    def create_messages_and_dialog(self, users, author=None, count=2):
        d = Dialog.objects.create()
        d.users.set(users)
        author = author if author is not None else users[0]
        for _ in range(count):
            Message.objects.create(text='test', author=author, dialog=d)

        return d

    def make_token(self, creds):
        res = self.client.post('/auth/jwt/create/',
                               data={'username': creds['username'],
                                     'password': creds['password']})
        return 'JWT ' + res.data['access']

    def login(self, creds=None):
        if creds is None:
            creds = self.current_user_creds
        token = self.make_token(creds)
        self.client.credentials(HTTP_AUTHORIZATION=token)


    def logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='')

    def get_user(self, n):
        return self.users[n]['user']

    def setUp(self) -> None:
        if self.need_to_login:
            self.login()
        return super().setUp()


class TestDialogView(LoginTestCase):

    def test_start_dialog_with_user(self):
        another_user = self.get_user(0)

        # Dialog with current and another user does not exists
        self.assertFalse(
            Dialog.objects.filter(users=self.current_user).filter(users=another_user).exists()
        )

        # dialog with current and another user was created
        res = self.client.post('/dialog/start_dialog_with_user/', data={'user_id': another_user.id})
        self.assertTrue(status.is_success(res.status_code))
        self.assertTrue(Dialog.objects.filter(id=res.data['id']).exists(), 'Dialog wasnt created')
        d = Dialog.objects.get(id=res.data['id'])
        users_in_dialog = list(d.users.all())

        #Check that current and another user in this dialog
        self.assertTrue(another_user in users_in_dialog and self.current_user in users_in_dialog,
                        f'users not take part in {d.id} dialog')

        # Check that we dont create new dialog ( with cur and another user) we retrieve that
        res = self.client.post('/dialog/start_dialog_with_user/', data={'user_id': another_user.id})
        self.assertTrue(d.id == res.data['id'], 'was created new dialog')

    def test_list_dialogs(self):
        # create two dialogs and only one in which current user take part
        self.create_messages_and_dialog((self.get_user(0), self.get_user(1)), count=1)
        self.create_messages_and_dialog((self.get_user(0), self.current_user), count=1)

        # Check that we get dialogs that contains messages
        my_dialogs_count = self.current_user.get_my_dialogs().count()
        res = self.client.get('/dialog/')
        self.assertTrue(res.data['count'] == my_dialogs_count, 'got wrong dialogs count')
        dialogs_count = len(list(takewhile(lambda d: len(d['messages']), res.data['results'])))
        self.assertTrue(my_dialogs_count == dialogs_count, 'got wrong dialogs count')

        #Created empty dialog and check that we dont get that dialog (that dialog not have messages)
        self.create_messages_and_dialog((self.get_user(0), self.current_user), count=0)
        res = self.client.get('/dialog/')
        self.assertTrue(res.data['count'] == my_dialogs_count,  'got wrong dialogs count')


class TestMessageView(LoginTestCase):

    def test_list_messages_viewed(self):
        count_msgs = 2
        d = self.create_messages_and_dialog([self.get_user(0), self.current_user],
                                            author=self.get_user(0), count=count_msgs)

        # Check that current user didnt view messages in this dialog
        self.assertFalse(d.messages.filter(who_viewed_it=self.current_user).exists())

        # Check that user viewed all messages in this dialog
        self.client.get(f'/dialog/{d.id}/message/')
        self.assertTrue(d.messages.filter(who_viewed_it=self.current_user).count() == count_msgs,
                        'user didnt view all messages in this dialog')

        ## Create new dialog and messages
        self.create_messages_and_dialog([self.get_user(0), self.current_user],
                                        author=self.get_user(0), count=count_msgs)

        ## Check that we have more than count_msgs messages
        self.assertTrue(Message.objects.count() > count_msgs)

        # Check that we get only those messages that belong this dialog
        res = self.client.get(f'/dialog/{d.id}/message/')
        self.assertTrue(len(res.data['results']) == count_msgs, 'got wrong count messages')
        msgs = MessageSerializer(d.messages.all(), many=True,
                                 context={'request': res.wsgi_request}).data
        self.assertEqual(msgs, res.data['results'], 'got wrong messages')

    def test_create_message(self):
        d = self.create_messages_and_dialog([self.current_user, self.get_user(0)], count=0)

        # check that current user is message author
        self.client.post(f'/dialog/{d.id}/message/', data={'dialog': d.id, 'text': 'test'})
        msg = d.messages.last()
        self.assertTrue(msg.author == self.current_user, 'user is not author')

    def test_only_participants_dialog_perm(self):

        # current user logout
        self.logout()
        d = self.create_messages_and_dialog([self.current_user, self.get_user(0)])

        # Check that unauthorized user can not get dialog messages
        res = self.client.get(f'/dialog/{d.id}/message/')
        self.assertTrue(res.status_code == status.HTTP_401_UNAUTHORIZED)

        # Check that authorized user which take part in this dialog can get messages
        self.login()
        res = self.client.get(f'/dialog/{d.id}/message/')
        self.assertTrue(status.is_success(res.status_code))

        # Check that current authorized user can not get dialog messages in which he not take part
        d2 = self.create_messages_and_dialog([self.get_user(0), self.get_user(1)])
        res = self.client.get(f'/dialog/{d2.id}/message/')
        self.assertTrue(res.status_code == status.HTTP_403_FORBIDDEN)
