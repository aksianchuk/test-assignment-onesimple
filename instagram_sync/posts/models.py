from django.core.validators import URLValidator
from django.db import models


class AbstractMedia(models.Model):
    """
    Абстрактный медиа-объект Instagram.

    Все поля с префиксом `ig_` соответствуют данным, полученным из API.

    Атрибуты:
        ig_id (CharField): Идентификатор.
        ig_media_type (CharField): Тип.
            - CAROUSEL_ALBUM (str): Альбом (несколько изображений и/или видео).
            - IMAGE (str): Изображение.
            - VIDEO (str): Видео.
        ig_media_url (TextField): URL-адрес.
        ig_timestamp (DateTimeField): Дата и время создания.
    """

    MEDIA_TYPE_CHOICES = {
        "CAROUSEL_ALBUM": "CAROUSEL_ALBUM",
        "IMAGE": "IMAGE",
        "VIDEO": "VIDEO",
    }

    ig_id = models.CharField(max_length=32, unique=True)
    ig_media_type = models.CharField(max_length=14, choices=MEDIA_TYPE_CHOICES)
    ig_media_url = models.TextField(validators=[URLValidator()])
    ig_timestamp = models.DateTimeField()

    class Meta:
        abstract = True


class Post(AbstractMedia):
    """
    Пост Instagram.

    Атрибуты:
        ig_caption (CharField): Подпись.
        ig_comments_count (PositiveIntegerField): Количество комментариев.
        ig_like_count (PositiveIntegerField): Количество лайков.
    """

    ig_caption = models.CharField(max_length=2200, blank=True)
    ig_comments_count = models.PositiveIntegerField()
    ig_like_count = models.PositiveIntegerField()


class ChildrenMedia(AbstractMedia):
    """
    Дочерний медиа-объект поста Instagram типа «Альбом».

    Атрибуты:
        post (Post): Пост, к которому относится дочерний медиа-объект.
    """

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="children_medias"
    )


class Comment(models.Model):
    """
    Комментарий к посту Instagram.

    Все поля с префиксом `ig_` соответствуют данным, полученным из API.

    Атрибуты:
        ig_id (CharField): Идентификатор.
        ig_text (CharField): Текст комментария.
        post (Post): Пост, к которому относится комментарий.
    """

    ig_id = models.CharField(max_length=32, unique=True)
    ig_text = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
