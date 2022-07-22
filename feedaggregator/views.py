from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from feedaggregator.forms import FeedForm
from django.urls import reverse_lazy
from feedaggregator.models import Feed
from users.models import Subscriber

# Why does LoginRequiredMixin have to go before CreateView?
class FeedFormView(LoginRequiredMixin, generic.CreateView):
  template_name = "feedaggregator/add.html"
  form_class = FeedForm
  # FIXME why is lazy necessary?
  success_url = reverse_lazy('feedaggregator:discover_feeds')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['user_first_name'] = self.request.user.first_name
    return context

class FeedDiscoverView(LoginRequiredMixin, generic.ListView):
  template_name = "feedaggregator/discover.html"
  context_object_name = "feeds"
  queryset = Feed.objects.all()
  paginate_by = 4

  def get_context_data(self, **kwargs):
    context = super(FeedDiscoverView, self).get_context_data(**kwargs)
    context["user_subscriptions"] = self.request.user.feed_set.all()
    return context

class FeedSubscriptionView(LoginRequiredMixin, generic.ListView):
  template_name = "feedaggregator/subscriptions.html"
  context_object_name = "subscriptions"

  def get_queryset(self):
    return self.request.user.feed_set.all()

class FeedSubscribeView(LoginRequiredMixin, generic.RedirectView):

  def get_redirect_url(self, *args, **kwargs):
    feed_pk = kwargs.get("feed_pk", None)
    if Feed.objects.get(pk=feed_pk):
      Feed.objects.get(pk=feed_pk).subscriptions.add(self.request.user)
    return self.request.META.get('HTTP_REFERER')

class FeedUnsubscribeView(LoginRequiredMixin, generic.RedirectView):

  def get_redirect_url(self, *args, **kwargs):
    feed_pk = kwargs.get("feed_pk", None)
    if Feed.objects.get(pk=feed_pk):
      Feed.objects.get(pk=feed_pk).subscriptions.remove(self.request.user)
    return self.request.META.get('HTTP_REFERER')