from django.shortcuts import render
from feedaggregator.models import Bookmark, Subscription
from rest_framework import viewsets
from api.serializers import BookmarkSerializer, SubscriptionSerializer

class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def list(self, request, **kwargs):
        self.queryset = self.queryset.filter(subscriber=request.user)
        return super().list(self, request, **kwargs)
    
class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
