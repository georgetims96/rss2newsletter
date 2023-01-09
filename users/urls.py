from django.urls import path
from django.views.generic import TemplateView
from users.views import RegisterCreateView, LoginView, LogoutView, GuestLoginRedirectView, NewLoginView

app_name = 'users'

urlpatterns = [
  path('register/', RegisterCreateView.as_view(), name='register'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout', LogoutView.as_view(), name='logout'),
  path('guest_login/', GuestLoginRedirectView.as_view(), name='guest_login'),
  path('new_login', NewLoginView.as_view(), name='new_login')
]