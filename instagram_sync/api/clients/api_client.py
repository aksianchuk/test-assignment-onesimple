from json.decoder import JSONDecodeError
from typing import Any, Dict

import requests
from django.conf import settings
from pydantic import ValidationError

from api.clients.exceptions import (
    InstagramApiClientBaseException,
    InstagramApiClientConnectionException,
    InstagramApiClientInvalidAccessTokenException,
    InstagramApiClientPostNotFoundException,
    InstagramApiClientResponseFormatException,
    InstagramApiClientTimeoutException,
)
from api.clients.schemas import (
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
        API_ERROR_EXCEPTION_MAP (dict): Словарь маппинга кодов ошибок API на
            соответствующие классы исключений.
    """

    API_URL = "https://graph.instagram.com/v25.0/"
    API_ACCESS_TOKEN = settings.INSTAGRAM_API_ACCESS_TOKEN
    API_CONNECT_TIMEOUT = 3
    API_REQUEST_TIMEOUT = 10
    API_ERROR_EXCEPTION_MAP = {
        100: InstagramApiClientPostNotFoundException,
        190: InstagramApiClientInvalidAccessTokenException,
    }

    def get_posts(self, next_url: str = None) -> MediaResponse:
        """
        Выполняет GET-запрос на получение постов пользователя.

        Аргументы:
            next_url (str): URL-адрес следующей страницы с постами.

        Возвращает:
            MediaResponse: Pydantic-модель с данными постов.
        """
        next_url = next_url or None
        if next_url:
            response_data = self._request("GET", str(next_url))
        else:
            response_data = self._request(
                "GET",
                f"{self.API_URL}me/media",
                {
                    "fields": (
                        "media_type,media_url,timestamp,caption,comments_count"
                        ",like_count,children{media_type,media_url,timestamp}"
                    )
                },
            )
        return MediaResponse(**response_data)

    def create_comment(
        self, post: int, text: str
    ) -> CreateCommentMediaResponse:
        """
        Выполняет POST-запрос на создание комментария к посту.

        Аргументы:
            post (int): Идентификатор поста.
            text (str): Текст комментария.

        Возвращает:
            CreateCommentMediaResponse: Pydantic-модель с данными созданного
                комментария.
        """

        payload = CreateCommentMediaRequest(media_id=str(post), message=text)
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
        if "access_token=" not in url:
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
                exception_class = self.API_ERROR_EXCEPTION_MAP.get(
                    error.error.code,
                    InstagramApiClientBaseException,
                )
                if exception_class is InstagramApiClientBaseException:
                    raise exception_class({"detail": error.model_dump()})
                raise exception_class
            response.raise_for_status()
            return response_data
        except ValidationError as error:
            raise InstagramApiClientBaseException({"detail": error.errors()})
        except JSONDecodeError:
            raise InstagramApiClientResponseFormatException
        except requests.exceptions.ConnectionError:
            raise InstagramApiClientConnectionException
        except requests.exceptions.Timeout:
            raise InstagramApiClientTimeoutException
        except requests.RequestException as error:
            raise InstagramApiClientBaseException(str(error))


client = InstagramApiClient()
