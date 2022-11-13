from django import template
from feedaggregator.models import Subscription

register = template.Library()

@register.filter
def feedToSubId(value, arg):
    return Subscription.objects.get(feed=value, user__id=arg).id