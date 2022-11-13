from django.shortcuts import render
from feedaggregator.models import Bookmark, Subscription
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import Http404
from api.serializers import BookmarkSerializer, SubscriptionSerializer
import json

class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def list(self, request, **kwargs):
        self.queryset = self.queryset.filter(subscriber=request.user)
        return super().list(self, request, **kwargs)
    
class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            feed_id = instance.feed.id
            self.perform_destroy(instance)
            return Response(status=201, data='{"feed": %r}' % feed_id)

        except Http404:
            pass
        