from tkinter import W
from django.db import models
from users.models import Subscriber

class Feed(models.Model):
  subscriptions = models.ManyToManyField(Subscriber)
  url = models.URLField(max_length=150, blank=False, unique=True)
  feed_encoding = models.CharField(max_length=150, blank=True, null=True)
  last_sent = models.DateTimeField(blank=True, null=True)

