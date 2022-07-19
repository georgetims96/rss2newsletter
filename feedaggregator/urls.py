from django.urls import path
from feedaggregator.views import FeedFormView

app_name = 'feedaggregator'

urlpatterns = [
  path('add/', FeedFormView.as_view(), name='add_feed')
]