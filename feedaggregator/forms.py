from django import forms
from django.contrib.auth.forms import UserCreationForm
from feedaggregator.models import Subscriber
from feedaggregator.models import Feed 

class FeedForm(forms.ModelForm):
  class Meta:
    model = Feed 
    fields = ['url']

class NewSubscriberForm(UserCreationForm):
  class Meta:
    model = Subscriber
    fields = ['email', 'first_name', 'second_name']
  
  def save(self, commit=True):
    subscriber = super(UserCreationForm, self).save(commit=False)
    subscriber.email = self.cleaned_data['email']
    if commit:
      subscriber.save()
    return subscriber
