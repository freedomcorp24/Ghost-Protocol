import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ghost_protocol.settings')

app = Celery('ghost_protocol')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
