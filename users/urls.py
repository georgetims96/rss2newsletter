from django.urls import path
from users.views import RegisterCreateView, LoginView, LogoutView, GuestLoginRedirectView

app_name = 'users'

urlpatterns = [
  path('register/', RegisterCreateView.as_view(), name='register'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout', LogoutView.as_view(), name='logout'),
  path('guest_login/', GuestLoginRedirectView.as_view(), name='guest_login')
]