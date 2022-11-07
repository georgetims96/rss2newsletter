from django.urls import include, path
from rest_framework import routers
from api.views import BookmarkViewSet

router = routers.DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet)

urlpatterns = [
    path('', include(router.urls))
]