from rest_framework.serializers import ModelSerializer

from api.models import Comment, Post, PostChild


class PostChildSerializer(ModelSerializer):
    """Сериализатор для дочерних постов Instagram."""

    class Meta:
        model = PostChild
        exclude = ("id", "post")


class PostSerializer(ModelSerializer):
    """Сериализатор для постов Instagram."""

    children = PostChildSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    """Сериализатор для комментариев к посту Instagram."""

    class Meta:
        model = Comment
        fields = ("id", "ig_id", "ig_text", "post")
        read_only_fields = ("ig_id", "post")
