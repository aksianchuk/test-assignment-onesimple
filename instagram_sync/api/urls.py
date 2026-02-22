from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import SyncPostsAPIView, PostsViewSet

router = SimpleRouter()

router.register("posts", PostsViewSet, basename="posts")
urlpatterns = [
    path("", include(router.urls)),
    path("sync/", SyncPostsAPIView.as_view()),
]
