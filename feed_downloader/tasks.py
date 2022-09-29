from __future__ import unicode_literals
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from feedaggregator.models import Feed, Entry
from datetime import datetime, timedelta
import pytz

@shared_task
def update_feeds():
  feeds = Feed.objects.all()
  # Loop through all feeds
  for feed in feeds:
    # Get entries from last 7 days
    # TODO need to have datetime be based on last sent
    feed_entries = feed.filter_entries(datetime.now(tz=pytz.utc) - timedelta(days=7))
    # Loop over relevant entries
    for entry in feed_entries:
      # Try to generate an entry
      try:
        new_entry = feed.generate_entry(entry)
        # Check if we've already pulled the entry
        if Entry.objects.filter(feed=feed, title=new_entry.title).count() == 0:
          # If we haven't, we should save it
          new_entry.save()
        else:
          # Otherwise, it exists
          print("exists")
          print(new_entry.feed)
          print(new_entry.title)
      except Exception as e:
        print(e)
    feed.last_sent = datetime.now(pytz.utc)
    feed.save()