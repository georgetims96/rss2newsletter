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

  def __str__(self):
    if self.title:
      return self.title
    return ""
  
  def send_email(self):
    # TODO move to newsletter_emailer app
    parsed_feed = feedparser.parse(self.url)
    feed_entries = parsed_feed["entries"]
    for entry in feed_entries:
      try:
        print(entry["content"][0]["value"])
        # print("-------------------")
      except:
        print(list(entry.keys()))

  def filter_entries(self, entries_since):
    '''
    Return all of the feed's entries since specified date
    '''
    pass
  def save(self, *args, **kwargs):
    # Only want to set title if new object
    if not self.pk:
      parsed_feed = feedparser.parse(self.url) 
      self.title = parsed_feed.feed.title
    self.send_email()
    super(Feed, self).save(*args, **kwargs)
  
class Subscription(models.Model):
  user = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
  feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
  date_subscribed = models.DateTimeField()

