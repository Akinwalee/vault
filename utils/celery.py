from celery import Celery
import os

os.environ.setdefault('CELERY_CONFIG', 'vault')

app = Celery('vault')

app.config_from_object('utils.celeryconfig')
app.autodiscover_tasks(['tasks'])