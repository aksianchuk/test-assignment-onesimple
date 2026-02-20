from typing import Any, Dict

import requests
from django.conf import settings

from schemas import (
    CreateCommentMediaRequest,
    CreateCommentMediaResponse,
    ErrorResponse,
    MediaResponse,
)


class InstagramApiClient:
    """
    Клиент для работы с API Instagram.

    Атрибуты:
        API_URL (str): Базовый URL для всех методов API.
        API_ACCESS_TOKEN (str): Токен доступа к API.
        API_CONNECT_TIMEOUT (int): Таймаут на установку соединения с сервером
            (по умолчанию 3).
        API_REQUEST_TIMEOUT (int): Таймаут на ожидание ответа от сервера (по
            умолчанию 10).
    """

    API_URL = "https://graph.instagram.com/v25.0/"
    API_ACCESS_TOKEN = settings.INSTAGRAM_API_ACCESS_TOKEN
    API_CONNECT_TIMEOUT = 3
    API_REQUEST_TIMEOUT = 10

    def get_posts(self) -> MediaResponse:
        """
        Выполняет GET-запрос на получение постов пользователя.

        Возвращает:
            MediaResponse: Pydantic-модель с данными постов.
        """

        response_data = self._request(
            "GET",
            f"{self.API_URL}me/media",
            {
                "fields": (
                    "id,media_type,media_url,timestamp,caption,comments_count,"
                    "like_count,children{id,media_type,media_url,timestamp}"
                )
            },
        )
        return MediaResponse(**response_data)

    def create_comment(
        self, post: str, text: str
    ) -> CreateCommentMediaResponse:
        """
        Выполняет POST-запрос на создание комментария к посту.

        Аргументы:
            post (str): Идентификатор поста.
            text (str): Текст комментария.

        Возвращает:
            CreateCommentMediaResponse: Pydantic-модель с данными созданного
                комментария.
        """

        payload = CreateCommentMediaRequest(media_id=post, message=text)
        response_data = self._request(
            "POST",
            f"{self.API_URL}{payload.media_id}/comments",
            {"message": payload.message},
        )
        return CreateCommentMediaResponse(**response_data)

    def _request(
        self, method: str, url: str, params: dict = None
    ) -> Dict[str, Any]:
        """
        Выполняет GET или POST-запрос к API.

        Аргументы:
            method (str): HTTP-метод.
            url (str): URL-адрес.
            params (dict): Параметры запроса.

        Возвращает:
            dict: Результат запроса.
        """

        params = params or {}
        params["access_token"] = self.API_ACCESS_TOKEN
        try:
            if method == "GET":
                response = requests.get(
                    url,
                    params=params,
                    timeout=(
                        self.API_CONNECT_TIMEOUT,
                        self.API_REQUEST_TIMEOUT,
                    ),
                )
            elif method == "POST":
                response = requests.post(
                    url,
                    params=params,
                    timeout=(
                        self.API_CONNECT_TIMEOUT,
                        self.API_REQUEST_TIMEOUT,
                    ),
                )
            else:
                raise ValueError(f"Неподдерживаемый HTTP метод: {method}")

            response_data = response.json()
            if "error" in response_data:
                error = ErrorResponse(**response_data)
                raise Exception(f"instagram_api_client: {error.model_dump()}")
            return response_data
        except requests.RequestException as error:
            raise Exception(f"instagram_api_client: {error}")


instagram_api_client = InstagramApiClient()
