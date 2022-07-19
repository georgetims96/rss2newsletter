from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy



class SubscriberManager(BaseUserManager):
  def create_user(self, email, first_name, second_name, password, **others):
    if not email:
      raise ValueError(gettext_lazy("You must provide an email address"))

    email = self.normalize_email(email)
    user = self.model(email=email, first_name=first_name, second_name=second_name, **others)
    user.set_password(password)
    user.save()
    return user
  
  def create_superuser(self, email, first_name, second_name, password, **others):
    others.setdefault("is_staff", True)
    others.setdefault("is_superuser", True)
    others.setdefault("is_active", True)

    if others.get("is_staff") is not True:
      raise ValueError("Superuser must be staff")
    if others.get("is_superuser") is not True:
      raise ValueError("Superuser must be superuser")
    return self.create_user(email, first_name, second_name, password, **others)


class Subscriber(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(gettext_lazy('email address'), unique=True)
  first_name = models.CharField(max_length=50, blank=False)
  second_name = models.CharField(max_length=50, blank=False)
# Trying to follow the existing Django flags
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  
  objects = SubscriberManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'second_name']

  def __str__(self):
    return f"{self.first_name} {self.second_name}"



