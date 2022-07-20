from django.shortcuts import render
from django.views import generic
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from feedaggregator.forms import FeedForm, NewSubscriberForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
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

@method_decorator(login_required, name='dispatch')
class FeedListView(generic.ListView):
  template_name = "feedaggregator/list.html"
  context_object_name = "feeds"
  queryset = Feed.objects.all()
  paginate_by = 10

class RegisterCreateView(generic.CreateView):
  form_class = NewSubscriberForm
  template_name = 'feedaggregator/register.html'
  success_url = reverse_lazy('feedaggregator:add_feed')

  def form_valid(self, form):
    valid = super().form_valid(form)
    email = form.cleaned_data.get('email')
    print(email)
    password = form.cleaned_data.get('password1')
    print(password)
    registered_user = authenticate(email=email, password=password)
    print(registered_user)
    login(self.request, registered_user)
    return valid

class LoginView(auth_views.LoginView):
  template_name = 'feedaggregator/login.html'
  redirect_authenticated_user = True

class LogoutView(auth_views.LogoutView):
  template_name = 'feedaggregator/logout.html'