from __future__ import unicode_literals
from __future__ import absolute_import, unicode_literals

from celery import shared_task

@shared_task
def add_task(a, b):
  return a + b