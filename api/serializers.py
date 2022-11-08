from rest_framework import serializers
from feedaggregator.models import Bookmark, Entry
from users.models import Subscriber

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