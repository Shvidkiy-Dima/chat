from django.db import models
from django.utils import timezone
from django.conf import settings
from chat_user.models import UserModel


class DialogManager(models.Manager):

    def get_or_create_dialog(self, user1, user2):
        dialogs = self.filter(users=user1).filter(users=user2)
        dialog, created = dialogs.get_or_create()
        if created:
            dialog.users.add(user1, user2)

        return dialog


class Dialog(models.Model):
    users = models.ManyToManyField(UserModel, related_name='dialogs')
    last_change = models.DateTimeField(default=timezone.now)

    objects = DialogManager()

    def get_last_message(self):
        return self.messages.first()

    class Meta:
        ordering = ['-last_change']


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name='messages')
    text = models.CharField(max_length=settings.MAX_LENGTH_MESSAGE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='my_msgs')
    who_viewed_it = models.ManyToManyField(UserModel)
    created = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.who_viewed_it.add(self.author)
        self.dialog.last_change = timezone.now()
        self.dialog.save(update_fields=['last_change'])

    def __str__(self):
        return self.text[:10]

    class Meta:
        ordering = ['-id']
