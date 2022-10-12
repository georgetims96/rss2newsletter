from django.contrib import admin
from feedaggregator.models import Bookmark, Feed, Subscription, Entry
# Register your models here.


admin.site.register(Feed)
admin.site.register(Subscription)
admin.site.register(Entry)
admin.site.register(Bookmark)
