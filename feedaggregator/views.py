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

class FeedSubscribeView(LoginRequiredMixin, generic.RedirectView):

  def get_redirect_url(self, *args, **kwargs):
    feed_pk = kwargs.get("feed_pk", None)
    rel_user = self.request.user
    rel_feed = Feed.objects.get(pk=feed_pk)
    if rel_feed and not Subscription.objects.filter(user=rel_user, feed=rel_feed).exists():
      Subscription.objects.create(
        user=self.request.user,
        feed=rel_feed,
        date_subscribed=datetime.now(timezone.utc)
      )
      rel_feed.num_subscribers = F('num_subscribers') + 1
      rel_feed.save()
    return self.request.META.get('HTTP_REFERER')
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["user_bookmarks"] = self.request.user.saved_entries.all()
    return context

class FeedUnsubscribeView(LoginRequiredMixin, generic.RedirectView):

  def get_redirect_url(self, *args, **kwargs):
    feed_pk = kwargs.get("feed_pk", None)
    rel_feed = Feed.objects.get(pk=feed_pk)
    if rel_feed:
      subscription_to_remove = Subscription.objects.get(
        user=self.request.user,
        feed__pk=feed_pk
      )
      subscription_to_remove.delete()
      # FIXME could I override delete method/do signal
      # FIXME is this the best way of dealing with this
      rel_feed.num_subscribers = F('num_subscribers') - 1
      rel_feed.save()
    return self.request.META.get('HTTP_REFERER')

class EntrySaveView(LoginRequiredMixin, generic.RedirectView):
  def get_redirect_url(self, *args, **kwargs):
    entry_pk = kwargs.get("entry_pk", None)
    rel_entry = Entry.objects.get(pk=entry_pk)
    if rel_entry:
      bookmark_to_add = Bookmark(
        subscriber = self.request.user,
        entry = rel_entry
      )
      bookmark_to_add.save()
    return self.request.META.get('HTTP_REFERER')

class EntryUnsaveView(LoginRequiredMixin, generic.RedirectView):
  def get_redirect_url(self, *args, **kwargs):
    entry_pk = kwargs.get("entry_pk", None)
    rel_entry = Entry.objects.get(pk=entry_pk)
    if rel_entry:
      bookmark_to_remove_qs = Bookmark.objects.filter(
        subscriber = self.request.user,
        entry = rel_entry
      )
      if bookmark_to_remove_qs.count() > 0:
        bookmark_to_remove_qs.delete()
    return self.request.META.get('HTTP_REFERER')

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
   