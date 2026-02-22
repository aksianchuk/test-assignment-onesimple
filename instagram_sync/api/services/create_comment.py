from api.clients.api_client import client
from api.models import Comment


def create_comment(post, text) -> Comment:
    """
    Создает комментарий к посту Instagram.

    Аргументы:
            post (Post): Объект поста.
            text (str): Текст комментария.

    Возвращает:
        Comment: Объект созданного комментария.
    """

    response = client.create_comment(post=post.ig_id, text=text)
    comment = Comment.objects.create(
        ig_id=response.id, ig_text=text, post=post
    )
    return comment
