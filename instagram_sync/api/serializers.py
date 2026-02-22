from rest_framework.serializers import ModelSerializer

from api.models import Post, PostChild, Comment


class PostChildSerializer(ModelSerializer):
    """Сериализатор для дочерних постов."""

    class Meta:
        model = PostChild
        exclude = ("id", "post")


class PostSerializer(ModelSerializer):
    """Сериализатор для постов."""

    children = PostChildSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    """Сериализатор для комментариев."""

    class Meta:
        model = Comment
        fields = ("id", "ig_id", "ig_text", "post")
        read_only_fields = ("ig_id", "post")
