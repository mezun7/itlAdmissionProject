# quick_publisher/celery.py

import os
from celery import Celery

from itlAdmissionProject import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itlAdmissionProject.settings')

app = Celery('itlAdmissionProject')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def hi():
    print('Hi')
