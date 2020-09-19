from django.db import models
from django.contrib.auth import get_user_model


class Dialog(models.Model):
    users = models.ManyToManyField(get_user_model())


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name='messages')
    text = models.CharField(max_length=512)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL)

