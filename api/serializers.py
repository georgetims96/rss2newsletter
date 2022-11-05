from rest_framework import serializers
from feedaggregator.models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['entry', 'subscriber']
        depth = 1