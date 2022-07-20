from django.urls import path
from feedaggregator.views import FeedFormView, FeedDiscoverView, FeedSubscribeView

app_name = 'feedaggregator'

urlpatterns = [
  path('add/', FeedFormView.as_view(), name='add_feed'),
  path('discover/', FeedDiscoverView.as_view(), name='discover_feeds'),
  path('subscribe/<feed_pk>', FeedSubscribeView.as_view(), name="subscribe_feeds")
]