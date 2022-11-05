from django.shortcuts import render
from feedaggregator.models import Bookmark
from rest_framework import viewsets
from api.serializers import BookmarkSerializer

class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
