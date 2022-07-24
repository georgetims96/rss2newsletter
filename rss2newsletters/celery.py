from __future__ import absolute_import, unicode_literals
# ^ makes sure celery.py module won't clash with library

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rss2newsletters.settings')

app = Celery('rss2newsletters')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()