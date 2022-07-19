from django.shortcuts import render
from django.views import generic
from feedaggregator.forms import FeedForm
from django.urls import reverse_lazy
# Create your views here.

class FeedFormView(generic.FormView):
  template_name = "feedaggregator/add.html"
  form_class = FeedForm
  # why is lazy necessary?
  success_url = reverse_lazy('feedaggregator:add_feed')
