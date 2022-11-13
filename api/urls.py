from django.urls import include, path
from rest_framework import routers
from api.views import BookmarkViewSet, SubscriptionViewSet



router = routers.DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet)
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls))
]