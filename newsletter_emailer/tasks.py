from __future__ import unicode_literals
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from datetime import datetime
from feedaggregator.models import Feed
from datetime import datetime, timezone, timedelta
@shared_task
def send_feeds():
  feeds = Feed.objects.all()
  # Loop through all feeds
  for feed in feeds:
    # Get entries from last 7 days
    # TODO need to have datetime be based on last sent
    # TODO datetiime not timezone aware
    feed_entries = feed.filter_entries(datetime.now() - timedelta(days=7))
    for entry in feed_entries:
      try:
        new_entry = feed.generate_entry(entry)
        new_entry.save()
      except(e):
        print(e)
    feed.last_sent = datetime.now()
    feed.save()