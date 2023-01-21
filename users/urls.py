from django.urls import path
from django.views.generic import TemplateView
from users.views import RegisterCreateView, LoginView, GuestLoginRedirectView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
  path('register/', RegisterCreateView.as_view(), name='register'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout', auth_views.LogoutView.as_view(), name='logout'),
  path('guest_login/', GuestLoginRedirectView.as_view(), name='guest_login'),
]