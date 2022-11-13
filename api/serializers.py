from rest_framework import serializers
from feedaggregator.models import Bookmark, Entry, Feed, Subscription
from users.models import Subscriber
from datetime import datetime, timezone

class BookmarkSerializer(serializers.ModelSerializer):
    entry = serializers.PrimaryKeyRelatedField(many=False, queryset=Entry.objects.all())
    subscriber = serializers.PrimaryKeyRelatedField(many=False, queryset=Subscriber.objects.all())

    class Meta:
        model = Bookmark
        fields = ['id', 'entry', 'subscriber']
        depth = 1
    
    def create(self, validated_data):
        return Bookmark.objects.create(
            entry=validated_data['entry'],
            subscriber=validated_data['subscriber']
        )

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'feed', 'user']
