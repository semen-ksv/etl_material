from __future__ import absolute_import
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_meatbase.settings')


app = Celery(__name__)
app.config_from_object('test_metabase:settings')
app.autodiscover_tasks()

TASK_SERIALIZER = 'json'
ACCEPT_CONTENT = ['json']

app.conf.update(
    BROKER_URL=settings.CELERY_BROKER_URL,
)

app.conf.beat_schedule = {
    # Executes every day at 5:30 a.m.
    'every-day_denormalize_data': {
        'task': 'api.services.denormalize_data',
        'schedule': crontab(minute=30, hour=5)
    },
}
