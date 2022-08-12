from django.contrib import admin
from feedaggregator.models import Feed, Subscription, Entry
# Register your models here.


admin.site.register(Feed)
admin.site.register(Subscription)
admin.site.register(Entry)
