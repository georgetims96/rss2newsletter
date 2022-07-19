from audioop import reverse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth import views as auth_views
from feedaggregator.forms import FeedForm, NewSubscriberForm
from django.urls import reverse_lazy

from feedaggregator.models import Subscriber

class FeedFormView(generic.CreateView):
  template_name = "feedaggregator/add.html"
  form_class = FeedForm
  # why is lazy necessary?
  success_url = reverse_lazy('feedaggregator:add_feed')

class RegisterCreateView(generic.CreateView):
  model = Subscriber
  form_class = NewSubscriberForm
  template_name = 'feedaggregator/register.html'
  success_url = reverse_lazy('feedaggregator:add_feed')

class LoginView(auth_views.LoginView):
  template_name = 'feedaggregator/login.html'
  redirect_authenticated_user = True