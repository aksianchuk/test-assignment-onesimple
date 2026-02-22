from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.models import Post
from api.pagination import PostCursorPagination
from api.serializers import CommentSerializer, PostSerializer
from api.services.create_comment import create_comment
from api.services.sync_posts import sync_posts


class SyncPostsAPIView(APIView):
    """APIView для синхронизации постов Instagram."""

    def post(self, request):
        response = sync_posts()
        return Response(response)


class PostsViewSet(ListModelMixin, GenericViewSet):
    """ViewSet для постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostCursorPagination

    @action(
        detail=True,
        methods=["post"],
        serializer_class=CommentSerializer,
    )
    def comment(self, request, *args, **kwargs):
        """Добавление комментария к посту."""

        post = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = create_comment(
            post, text=serializer.validated_data["ig_text"]
        )
        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
