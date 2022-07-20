from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from feedaggregator.forms import FeedForm
from django.urls import reverse_lazy
from feedaggregator.models import Feed

# Why does LoginRequiredMixin have to go before CreateView?
class FeedFormView(LoginRequiredMixin, generic.CreateView):
  template_name = "feedaggregator/add.html"
  form_class = FeedForm
  # FIXME why is lazy necessary?
  success_url = reverse_lazy('feedaggregator:view_feeds')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['user_first_name'] = self.request.user.first_name
    return context

class FeedListView(LoginRequiredMixin, generic.ListView):
  template_name = "feedaggregator/list.html"
  context_object_name = "feeds"
  queryset = Feed.objects.all()
  paginate_by = 10
