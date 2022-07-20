from django.db import models
from users.models import Subscriber
import feedparser

class Feed(models.Model):
  subscriptions = models.ManyToManyField(Subscriber)
  title = models.CharField(max_length=150, blank=True, null=True)
  url = models.URLField(max_length=150, blank=False, unique=True)
  feed_encoding = models.CharField(max_length=150, blank=True, null=True)
  last_sent = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    if self.title:
      return self.title
    return ""

  def save(self, *args, **kwargs):
    # Only want to set title if new object
    if not self.pk:
      parsed_feed = feedparser.parse(self.url) 
      self.title = parsed_feed.feed.title
    super(Feed, self).save(*args, **kwargs)
  
