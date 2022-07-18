from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Subscriber(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(_('email address'), unique=True)
  first_name = models.CharField(max_length=50, blank=False)
  second_name = models.CharField(mac_length=50, blank=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(defailt=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

class SubscriberManager(BaseUserManager):
  def create_user(self, email, first_name, second_name, password, **others):
    if not email:
      raise ValueError("You must provide an email address")

    email = self.normalize_email(email)
    user = self.model(first_name=first_name, second_name=second_name, **others)
    user.set_password(password)
    user.save()
    return user
  
  def create_superuser(self, email, first_name, second_name, password, **others):
    others.setdefault("is_staff", True)
    others.setdefault("is_superuser", True)
    others.setdefault("is_active", True)
