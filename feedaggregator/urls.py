from django.urls import path
from feedaggregator.views import *

app_name = 'feedaggregator'

urlpatterns = [
  path('', FeedDiscoverView.as_view(), name='home_view'),
  path('add/', FeedFormView.as_view(), name='add_feed'),
  path('discover/', FeedDiscoverView.as_view(), name='discover_feeds'),
  path('subscribe/<feed_pk>', FeedSubscribeView.as_view(), name="subscribe_feed"),
  path('unsubscribe/<feed_pk>', FeedUnsubscribeView.as_view(), name="unsubscribe_feed"),
  path('view/', FeedSubscriptionView.as_view(), name="view_feeds"),
  path('entries/<feed_pk>', EntryListView.as_view(), name='entry_list'),
  path('entry/<pk>', EntryDetailView.as_view(), name='entry_detail'),
  path('bookmark/<entry_pk>', EntrySaveView.as_view(), name='bookmark_entry'),
  path('unbookmark/<entry_pk>', EntryUnsaveView.as_view(), name='unbookmark_entry'),
  path('bookmarks/', EntrySavedView.as_view(), name='bookmarks'),
]