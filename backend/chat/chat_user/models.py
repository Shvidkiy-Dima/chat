from django.contrib.auth.models import AbstractUser


class ChatUser(AbstractUser):


    def __str__(self):
        return f'user_{self.id}'