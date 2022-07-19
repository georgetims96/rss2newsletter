from django.urls import path
from feedaggregator.views import FeedFormView, RegisterCreateView, RegisterFormView

app_name = 'feedaggregator'

urlpatterns = [
  path('add/', FeedFormView.as_view(), name='add_feed'),
  path('register/', RegisterCreateView.as_view(), name='register')
]