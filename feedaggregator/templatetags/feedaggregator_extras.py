from django import template
from feedaggregator.models import Subscription

register = template.Library()

@register.filter
def feedToSubId(value, arg):
    # FIXME GET should work given unique constraint, which I need to add
    return Subscription.objects.filter(feed=value, user__id=arg).first().id