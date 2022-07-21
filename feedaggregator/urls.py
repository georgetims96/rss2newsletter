from django.urls import path
from feedaggregator.views import FeedFormView, FeedDiscoverView, FeedSubscribeView, FeedSubscriptionView, FeedUnsubscribeView

app_name = 'feedaggregator'

urlpatterns = [
  path('add/', FeedFormView.as_view(), name='add_feed'),
  path('discover/', FeedDiscoverView.as_view(), name='discover_feeds'),
  path('subscribe/<feed_pk>', FeedSubscribeView.as_view(), name="subscribe_feed"),
  path('unsubscribe/<feed_pk>', FeedUnsubscribeView.as_view(), name="unsubscribe_feed"),
  path('view/', FeedSubscriptionView.as_view(), name="view_feeds")
]