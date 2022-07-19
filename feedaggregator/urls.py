from django.urls import path
from feedaggregator.views import FeedFormView, RegisterCreateView, LoginView, LogoutView, FeedListView

app_name = 'feedaggregator'

urlpatterns = [
  path('add/', FeedFormView.as_view(), name='add_feed'),
  path('view/', FeedListView.as_view(), name='view_feeds'),
  path('register/', RegisterCreateView.as_view(), name='register'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout', LogoutView.as_view(), name='logout')
]