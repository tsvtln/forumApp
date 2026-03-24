from __future__ import absolute_import, unicode_literals
import os
from pickle import TRUE

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forumApp.settings')
app = Celery('forumApp')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
