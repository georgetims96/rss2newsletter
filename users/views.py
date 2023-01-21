from django.views import generic
from django.views.generic.base import RedirectView
from users.forms import NewSubscriberForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy

class RegisterCreateView(generic.CreateView):
  form_class = NewSubscriberForm
  template_name = 'users/register.html'
  success_url = reverse_lazy('feedaggregator:add_feed')

  def form_valid(self, form):
    valid = super().form_valid(form)
    email = form.cleaned_data.get('email')
    password = form.cleaned_data.get('password1')
    registered_user = authenticate(email=email, password=password)
    login(self.request, registered_user)
    return valid

class LoginView(auth_views.LoginView):
  template_name = 'users/login.html'
  redirect_authenticated_user = True

class GuestLoginRedirectView(RedirectView):
  pattern_name = 'feedaggregator:discover_feeds'

  def get_redirect_url(self, *args, **kwargs):
    guest_user = authenticate(self.request, email="guest@gmail.com", password="Guestpassword123*")
    login(self.request, guest_user)
    return super().get_redirect_url(*args, **kwargs)
