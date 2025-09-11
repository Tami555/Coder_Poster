import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Coder.settings')
app = Celery('Coder')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()