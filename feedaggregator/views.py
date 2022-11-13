from ast import Sub
from django.views import generic
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from feedaggregator.forms import FeedForm
from django.urls import reverse_lazy
from feedaggregator.models import Feed, Subscription, Entry, Bookmark
from users.models import Subscriber
from datetime import datetime, timezone
from django.shortcuts import redirect

# Why does LoginRequiredMixin have to go before CreateView?
# TODO add Entry view!!!
class FeedFormView(LoginRequiredMixin, generic.CreateView):
  template_name = "feedaggregator/add.html"
  form_class = FeedForm
  # FIXME why is lazy necessary?
  success_url = reverse_lazy('feedaggregator:discover_feeds')

  def get(self, *args, **kwargs):
    # FIXME If we're doing this, maybe we don't need a LoginRequiredMixin
    if not self.request.user.is_superuser:
      return redirect(reverse_lazy('feedaggregator:discover_feeds'))
    return super(FeedFormView, self).get(*args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['user_first_name'] = self.request.user.first_name
    return context

class FeedDiscoverView(LoginRequiredMixin, generic.ListView):
  template_name = "feedaggregator/discover.html"
  context_object_name = "feeds"
  queryset = Feed.objects.all()
  paginate_by = 6 

  def get_context_data(self, **kwargs):
    context = super(FeedDiscoverView, self).get_context_data(**kwargs)
    context["user_subscriptions"] = self.request.user.subscriptions.all()
    return context

class FeedSubscriptionView(LoginRequiredMixin, generic.ListView):
  template_name = "feedaggregator/subscriptions.html"
  context_object_name = "subscriptions"

  def get_queryset(self):
    return Subscription.objects.filter(user=self.request.user)

class EntrySavedView(LoginRequiredMixin, generic.ListView):
  context_object_name = "saved_entries"
  template_name = "feedaggregator/saved_entries.html"
  paginate_by = 10 
  
  def get_queryset(self):
    return Bookmark.objects.filter(subscriber=self.request.user)

class EntryListView(LoginRequiredMixin, generic.ListView):
  model = Entry
  template_name = "feedaggregator/entry_list.html"
  context_object_name = "entries"
  ordering = ['-pk']
  paginate_by = 10 

  def get_queryset(self):
    queryset = Entry.objects.filter(feed__id=self.kwargs['feed_pk'])
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # FIXME non-existent feed guarding
    context['feed_title'] = Feed.objects.get(id=self.kwargs['feed_pk']).title
    return context


class EntryDetailView(LoginRequiredMixin, generic.DetailView):
  model = Entry
  template_name = "feedaggregator/entry_detail.html"
  context_object_name = "entry"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    bm = Bookmark.objects.filter(subscriber=self.request.user, entry=context["entry"])
    context["user_did_bookmark"] = True if bm.count() else False
    context['bookmark_id'] = bm.first().id if bm.count() else ""
    return context
