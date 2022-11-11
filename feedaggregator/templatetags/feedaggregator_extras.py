from django import template

register = template.Library()

@register.filter
def feedToSubId(value, arg):
    return None