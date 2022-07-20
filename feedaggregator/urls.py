from django.urls import path
from feedaggregator.views import FeedFormView, FeedListView

app_name = 'feedaggregator'

urlpatterns = [
  path('add/', FeedFormView.as_view(), name='add_feed'),
  path('view/', FeedListView.as_view(), name='view_feeds'),
]