import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cityMap.settings')
app = Celery('city')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Set broker_connection_retry_on_startup to True
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()
