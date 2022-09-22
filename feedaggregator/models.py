from ast import parse
from django.db import models
from users.models import Subscriber
import feedparser
from datetime import datetime
import pytz
from time import mktime
import html

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

  class Meta:
    ordering = ['title']
  
  def __str__(self):
    if self.title:
      return self.title
    return ""
  
  def generate_entry(self, raw_entry):
    '''
    Create Entry object given raw entry from parsed feed
    '''
    # TODO create Mail object and add to newsletter_emailer
    # Get the parsed feeds' entries
    new_entry = Entry(
      feed=self,
    )
    if self.content_key == "content":
      new_entry.body = html.unescape(raw_entry["content"][0]["value"])
      new_entry.published_date = self.st_to_dt(raw_entry['published_parsed'])
      new_entry.title = raw_entry["title"]
      new_entry.save()
    elif self.content_key == "summary":
      new_entry.body = html.unescape(raw_entry["summary"])
      new_entry.published_date = self.st_to_dt(raw_entry['published_parsed'])
      new_entry.title = raw_entry["title"]
    return new_entry

  def st_to_dt(self, st):
    # Generate datetime object from passed time struct
    # FIXME tz=pytz.utc does not work for some reason
    rel_datetime = datetime.fromtimestamp(mktime(st), tz=pytz.utc)
    print(rel_datetime.tzinfo)
    return datetime.fromtimestamp(mktime(st), tz=pytz.utc)

  def filter_entries(self, entries_since_date):
    '''
    Return all of the feed's entries since specified date

    :param entries_since_date: datetime object that represents the cutoff date for entries
    
    :return: list of entries published since specified date
    '''
    parsed_feed = feedparser.parse(self.url)
    return [x for x in parsed_feed['entries'] \
      if self.st_to_dt(x['published_parsed']) > entries_since_date]


  def save(self, *args, **kwargs):
    # Only want to set title if new object
    if not self.pk:
      # Get the feed's title and check its structure
      # Some have article body text in "content" tag; other's in "description"/"summary"
      parsed_feed = feedparser.parse(self.url) 
      self.title = parsed_feed.feed.title
      if "entries" in parsed_feed and len(parsed_feed["entries"]) > 0:
        if "content" in parsed_feed["entries"][0]:
          self.content_key = "content"
        elif "summary" in parsed_feed["entries"][0]:
          self.content_key = "summary"
        # Check if entries are sorted normally
        first_entry_date = self.st_to_dt(parsed_feed["entries"][0]["published_parsed"])
        second_entry_date = self.st_to_dt(parsed_feed["entries"][1]["published_parsed"])
        if first_entry_date < second_entry_date:
          # If they aren't mark the feed as such
          self.sorted_normal = False
    super(Feed, self).save(*args, **kwargs)
  
class Entry(models.Model):
  feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
  published_date = models.DateTimeField(null=True, default=None)
  title = models.CharField(max_length=254)
  body = models.TextField()
  
  class Meta:
    verbose_name_plural = "entries"
    
class Subscription(models.Model):
  user = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
  feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
  date_subscribed = models.DateTimeField()

  def __str__(self):
    return self.feed.title

  class Meta:
    ordering = ['date_subscribed']

