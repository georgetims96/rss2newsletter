from __future__ import unicode_literals
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from feedaggregator.models import Feed
from datetime import datetime, timedelta
import pytz
import sendgrid

# TODO set up cron job for emails!