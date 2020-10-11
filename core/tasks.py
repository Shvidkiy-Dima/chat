from logging import getLogger
from django.db.models import Count
from celery import shared_task
from .models import Dialog

logger = getLogger('base')


@shared_task
def delete_inactive_dialogs():
    inactive_dialogs = Dialog.objects.annotate(msgs=Count('messages')).filter(msgs=0)
    logger.info(f'Will be deleted {inactive_dialogs.count()} inactive dialogs')
    inactive_dialogs.delete()