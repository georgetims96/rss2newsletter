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
  content_key = models.CharField(max_length=25, default="invalid")
  # Checks if RSS entries are sorted most recent first (i.e. True)
  sorted_normal = models.BooleanField(default=True)

  def __str__(self):
    if self.title:
      return self.title
    return ""
  
  def send_email(self):
    # TODO create Mail object and add to newsletter_emailer
    # Parse the relevant feed
    parsed_feed = feedparser.parse(self.url)
    # Get the parsed feeds' entries
    feed_entries = parsed_feed["entries"]
    # Loop over parsed feeds' entries
    for entry in feed_entries:
      if self.content_key == "content":
        print(entry["content"][0]["value"])
      elif self.content_key == "summary":
        print("here")
        print(entry["summary"])
      # print("-------------------")

  def filter_entries(self, entries_since):
    '''
    Return all of the feed's entries since specified date
    '''
    parsed_feed = feedparser.parse(self.url)

  def save(self, *args, **kwargs):
    # Only want to set title if new object
    if not self.pk:
      # Get the feed's title and check its structure
      # i.e. it's not just summaries of articles
      parsed_feed = feedparser.parse(self.url) 
      self.title = parsed_feed.feed.title
      if "entries" in parsed_feed and len(parsed_feed["entries"]) > 0:
        if "content" in parsed_feed["entries"][0]:
          self.content_key = "content"
        elif "summary" in parsed_feed["entries"][0]:
          self.content_key = "summary"

    # Check if entries are sorted normally
    # FIXME remove
    self.send_email()
    super(Feed, self).save(*args, **kwargs)
  
class Subscription(models.Model):
  user = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
  feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
  date_subscribed = models.DateTimeField()

