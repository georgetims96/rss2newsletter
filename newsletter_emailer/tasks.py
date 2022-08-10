from __future__ import unicode_literals
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from datetime import datetime
from feedaggregator.models import Feed

@shared_task
def send_feeds():
  feeds = Feed.objects.all()
  # Loop through all feeds
  for feed in feeds:
    # Send an email
    feed.send_email()
    # Update feed's last sent attribute accordingly
    feed.last_sent = datetime.now()
    feed.save()