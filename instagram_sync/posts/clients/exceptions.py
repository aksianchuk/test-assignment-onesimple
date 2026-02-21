from rest_framework import status
from rest_framework.exceptions import APIException


class InstagramApiClientBaseException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class InstagramApiClientResponseFormatException(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "Невалидный JSON ответ от Instagram API"


class InstagramApiClientConnectionException(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Не удалось подключиться к Instagram API"


class InstagramApiClientTimeoutException(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Превышен лимит на соединение или ответ от Instagram API"
