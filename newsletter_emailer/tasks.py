from __future__ import unicode_literals
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from feedaggregator.models import Feed, Entry
from users.models import Subscriber
from newsletter_emailer.models import EmailHistory
from datetime import datetime, timedelta
import pytz
import sendgrid

@shared_task
def send_entries():
    # Get all Feeds
    feeds = Feed.objects.all()
    # Loop over each feed
    for feed in feeds:
        # Get the relevant (i.e. unsent) entries
        entries_to_send = Entry.objects.filter(feed=feed, sent=False)
        # Get the subscribers to the feed
        if entries_to_send.count() > 0:
            rel_subscribers = Subscriber.objects.filter(subscriptions=feed) 
            for entry in entries_to_send:
                # Loop over each entry, sending each one to the relevant recipients
                email_to_send = EmailHistory(rel_subscribers, entry)
                email_to_send.send()