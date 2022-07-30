from django.db import models
from users.models import Subscriber
import feedparser


class Feed(models.Model):
  subscriptions = models.ManyToManyField(Subscriber)
  title = models.CharField(max_length=150, blank=True, null=True)
  url = models.URLField(max_length=150, blank=False, unique=True, verbose_name="URL")
  feed_encoding = models.CharField(max_length=150, blank=True, null=True)
  last_sent = models.DateTimeField(blank=True, null=True)
  subscribers = models.ManyToManyField(Subscriber, through='Subscription', related_name="subscriptions")
  abbreviated = models.BooleanField(default=True)

  def __str__(self):
    if self.title:
      return self.title
    return ""
  
  def send_email(self):
    # TODO create Mail object and add to newsletter_emailer
    # Only send emails for comprehensive feeds
    if not self.abbreviated:
      # Parse the relevant feed
      parsed_feed = feedparser.parse(self.url)
      # Get the parsed feeds' entries
      feed_entries = parsed_feed["entries"]
      # Loop over parsed feeds' entries
      for entry in feed_entries:
        print(entry["content"][0]["value"])
        # print("-------------------")

  def filter_entries(self, entries_since):
    '''
    Return all of the feed's entries since specified date
    '''
    pass
  def save(self, *args, **kwargs):
    # Only want to set title if new object
    if not self.pk:
      # Get the feed's title and check if it's a comprehensive feed
      # i.e. it's not just summaries of articles
      parsed_feed = feedparser.parse(self.url) 
      self.title = parsed_feed.feed.title
      if "entries" in parsed_feed and "content" in parsed_feed["entries"][0]:
        self.abbreviated = False

    # FIXME remove
    self.send_email()
    super(Feed, self).save(*args, **kwargs)
  
class Subscription(models.Model):
  user = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
  feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
  date_subscribed = models.DateTimeField()

