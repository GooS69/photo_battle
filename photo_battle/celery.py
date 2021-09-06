import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photo_battle.settings')

app = Celery('photo_battle')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
