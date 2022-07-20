from django.contrib.auth.forms import UserCreationForm
from users.models import Subscriber

class NewSubscriberForm(UserCreationForm):
  class Meta:
    model = Subscriber
    fields = ['email', 'first_name', 'second_name', 'password1', 'password2'] 