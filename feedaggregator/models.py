from ast import parse
from django.db import models
from users.models import Subscriber
import feedparser
from datetime import datetime
from time import mktime
import feedaggregator.utils as utils

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

  def filter_entries(self, entries_since_date):
    '''
    Return all of the feed's entries since specified date

    :param entries_since_date: datetime object that represents the cutoff date for entries
    
    :return: list of entries published since specified date
    '''
    parsed_feed = feedparser.parse(self.url)
    num_entries = len(parsed_feed["entries"])
    # Case where entries are sorted normally
    if self.sorted_normal:
      # Tracker variable
      idx = num_entries - 1
      # Keep decrementing tracker variable until we find an entry before the cutoff date
      while self.st_to_dt(parsed_feed["entries"][idx]["published_parsed"]) >= entries_since_date and idx >= 0:
        idx -= 1
      # Return relevant slice of entries
      return parsed_feed["entries"][(idx + 1):]
    # Case where entries are sorted oldest first
    else:
      idx = 0
      while self.st_to_dt(parsed_feed["entries"][idx]["published_parsed"]) < entries_since_date and idx < num_entries:
        idx += 1
      return parsed_feed["entries"][idx:]

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
        first_entry_date = utils.st_to_dt(parsed_feed["entries"][0]["published_parsed"])
        second_entry_date = utils.st_to_dt(parsed_feed["entries"][1]["published_parsed"])
        if first_entry_date < second_entry_date:
          # If they aren't mark the feed as such
          self.sorted_normal = False
      

    # FIXME remove
    # self.send_email()
    super(Feed, self).save(*args, **kwargs)
  
class Subscription(models.Model):
  user = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
  feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
  date_subscribed = models.DateTimeField()

