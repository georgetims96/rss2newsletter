from django.views import generic
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

class LogoutView(auth_views.LogoutView):
  template_name = 'users/logout.html'