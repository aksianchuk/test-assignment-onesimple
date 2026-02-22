from django.db import transaction
from rest_framework import status

from api.clients.api_client import client
from api.models import Post, PostChild


def sync_posts() -> tuple[dict[str, str], int]:
    """
    Выполняет синхронизацию постов Instagram.

    Возвращает:
        tuple[dict[str, str], int]: сообщение и статус операции.
    """

    response = client.get_posts()
    if response.data:
        posts = []
        posts_children = []
        while True:
            for media in response.data:
                post = Post(
                    ig_id=media.id,
                    ig_media_type=media.media_type,
                    ig_media_url=media.media_url,
                    ig_timestamp=media.timestamp,
                    ig_caption=media.caption,
                    ig_comments_count=media.comments_count,
                    ig_like_count=media.like_count,
                )
                posts.append(post)
                if media.children:
                    for child_media in media.children.data:
                        posts_children.append(
                            PostChild(
                                ig_id=child_media.id,
                                ig_media_type=child_media.media_type,
                                ig_media_url=child_media.media_url,
                                ig_timestamp=child_media.timestamp,
                                post=post,
                            )
                        )
            if not response.paging.next:
                break
            response = client.get_posts(response.paging.next)
        with transaction.atomic():
            Post.objects.bulk_create(
                posts,
                update_conflicts=True,
                update_fields=[
                    "ig_media_type",
                    "ig_media_url",
                    "ig_timestamp",
                    "ig_caption",
                    "ig_comments_count",
                    "ig_like_count",
                ],
                unique_fields=["ig_id"],
            )
            PostChild.objects.bulk_create(
                posts_children,
                update_conflicts=True,
                update_fields=[
                    "ig_media_type",
                    "ig_media_url",
                    "ig_timestamp",
                ],
                unique_fields=["ig_id"],
            )
        return {"message": "Синхронизация прошла успешно"}, status.HTTP_200_OK
    return {
        "message": "В профиле отсутствуют посты"
    }, status.HTTP_400_BAD_REQUEST
