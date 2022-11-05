from rest_framework import serializers
from feedaggregator.models import Bookmark

class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['entry', 'subscriber']