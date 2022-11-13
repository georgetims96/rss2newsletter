from django.urls import path, include
from feedaggregator.views import *

app_name = 'feedaggregator'

urlpatterns = [
  path('', FeedDiscoverView.as_view(), name='home_view'),
  path('add/', FeedFormView.as_view(), name='add_feed'),
  path('discover/', FeedDiscoverView.as_view(), name='discover_feeds'),
  path('view/', FeedSubscriptionView.as_view(), name="view_feeds"),
  path('entries/<feed_pk>', EntryListView.as_view(), name='entry_list'),
  path('entry/<pk>', EntryDetailView.as_view(), name='entry_detail'),
  path('bookmarks/', EntrySavedView.as_view(), name='bookmarks'),
]