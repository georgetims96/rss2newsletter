from django import forms
from feedaggregator.models import Feed 

class FeedForm(forms.ModelForm):
  class Meta:
    model = Feed 
    fields = ['url']