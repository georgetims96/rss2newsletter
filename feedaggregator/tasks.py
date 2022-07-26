from __future__ import unicode_literals
from __future__ import absolute_import, unicode_literals

from django.db import connection
from celery import shared_task

from feedaggregator.models import Feed

@shared_task
def send_feeds():
  feeds = Feed.objects.all()
  feed_emails = []
  for feed in feeds:
    try:
      feed.send_email()
      feed_emails.append(feed)
    except:
      print(f"{feed.title} FAILED TO SEND")
  return feed_emails