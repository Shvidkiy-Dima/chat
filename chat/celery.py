import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

CeleryApp = Celery('chat')
CeleryApp.config_from_object('django.conf:settings', namespace='CELERY')
CeleryApp.autodiscover_tasks()
