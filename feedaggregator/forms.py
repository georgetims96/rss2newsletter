from django import forms
from django.core.exceptions import ValidationError
from feedaggregator.models import Feed 
import feedparser

class FeedForm(forms.ModelForm):
  class Meta:
    model = Feed 
    fields = ['url']
    widgets = {
      'url': forms.TextInput,
    }
  
  def clean_url(self):
    '''
    Check that provided URL is a valid RSS feed
    '''
    clean_data = self.cleaned_data.get('url')
    feed_data = feedparser.parse(clean_data)
    if feed_data.bozo:
      raise ValidationError("Please enter valid RSS feed.")
    return clean_data
