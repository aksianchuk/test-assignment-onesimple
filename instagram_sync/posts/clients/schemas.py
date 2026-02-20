from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class BaseMedia(BaseModel):
    """
    Схема базового медиа-объекта Instagram.

    Атрибуты:
        id: Идентификатор.
        media_type: Тип.
            - CAROUSEL_ALBUM: Альбом (несколько изображений и/или видео).
            - IMAGE: Изображение.
            - VIDEO: Видео.
        media_url: URL-адрес.
        timestamp: Дата и время создания.
    """

    id: str | None = Field(max_length=32)
    media_type: Literal["CAROUSEL_ALBUM", "IMAGE", "VIDEO"] | None
    media_url: HttpUrl | None
    timestamp: datetime | None


class MediaFieldsChildrenField(BaseModel):
    """
    Схема дочерних полей медиа-объекта.

    Атрибуты:
        data: Список объектов BaseMedia.
    """

    data: list[BaseMedia] | None


class MediaFieldsField(BaseMedia):
    """
    Схема дополнительных полей медиа-объекта.

    Атрибуты:
        caption: Подпись.
        comments_count: Количество комментариев.
        like_count: Количество лайков.
        children: Объект MediaFieldsChildrenField.
    """

    caption: str | None = Field(max_length=2200, default=None)
    comments_count: int
    like_count: int
    children: MediaFieldsChildrenField | None = None


class MediaRequest(BaseModel):
    """
    Схема запроса медиа-объекта.

    Атрибуты:
        media_id: Идентификатор.
        fields: Объект MediaFieldsField.
    """

    media_id: str
    fields: MediaFieldsField | None = None


class MediaResponsePagingCursorField(BaseModel):
    """
    Схема полей с идентификаторами начала и конца страницы при получении
    медиа-объекта.

    Атрибуты:
        before: Идентификатор начала текущей страницы.
        after: Идентификатор конца текущей страницы.
    """

    before: str
    after: str


class MediaResponsePagingField(BaseModel):
    """
    Схема полей пагинации при получении медиа-объекта.

    Атрибуты:
        cursors: Объект MediaResponsePagingCursorField.
        next: URL-адрес для запроса следующей страницы ответа.
    """

    cursors: MediaResponsePagingCursorField | None
    next: HttpUrl | None = None


class MediaResponse(BaseModel):
    """
    Схема ответа получения медиа-объекта.

    Атрибуты:
        data: Список объектов MediaFieldsField.
        paging: Объект MediaResponsePagingField.
    """

    data: list[MediaFieldsField] | None
    paging: MediaResponsePagingField = None


class CreateCommentMediaRequest(BaseModel):
    """
    Схема создания комментария к медиа-объекту.

    Атрибуты:
        media_id: Идентификатор.
        message: Текст комментария.
    """

    media_id: str
    message: str = Field(min_length=1, max_length=2200)


class CreateCommentMediaResponse(BaseModel):
    """
    Схема ответа при создании комментария к медиа-объекту.

    Атрибуты:
        id: Идентификатор созданного комментария.
    """

    id: str


class ErrorResponseErrorField(BaseModel):
    """
    Схема полей при ошибке(ах).

    Атрибуты:
        message: Описание ошибки.
        type: Тип ошибки.
        code: Код ошибки.
        error_code: Код дополнительной информации об ошибке.
        is_transient: Временная/постоянная ошибка.
        error_user_title: Заголовок ошибки для пользователя.
        error_user_msg: Описание ошибки для пользователя.
        fbtrace_id: Внутренний идентификатор для получения техподдержки.
    """

    message: str | None = None
    type: str | None = None
    code: int | None = None
    error_code: int | None = None
    is_transient: bool | None = None
    error_user_title: str | None = None
    error_user_msg: str | None = None
    fbtrace_id: str | None = None


class ErrorResponse(BaseModel):
    """
    Схема ответа при ошибке(ах).

    Атрибуты:
        error: Объект ErrorResponseErrorField.
    """

    error: ErrorResponseErrorField | None
