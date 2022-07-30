from __future__ import unicode_literals
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from feedaggregator.models import Feed

@shared_task
def send_feeds():
  feeds = Feed.objects.all()
  for feed in feeds:
    feed.send_email()
    print("DONE")