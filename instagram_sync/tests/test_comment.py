import pytest
from django.urls import reverse
from rest_framework import status

from api.models import Comment, Post


@pytest.mark.django_db
def test_create_comment_success(
    api_client, requests_mock, api_url, access_token, post, comment_post_url
):
    """
    Проверяет создание записи в базе и корректность ответа API при успешном
    запросе на создание комментария к посту Instagram.
    """

    comment_id = 1
    comment_ig_id = "12345678912345678"
    comment_ig_text = "Text"
    requests_mock.post(
        f"{api_url}{post.ig_id}/comments?message={comment_ig_text}"
        f"&access_token={access_token}",
        json={"id": comment_ig_id},
    )
    assert Comment.objects.count() == 0
    response = api_client.post(comment_post_url, {"ig_text": comment_ig_text})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {
        "id": comment_id,
        "ig_id": comment_ig_id,
        "ig_text": comment_ig_text,
        "post": post.id,
    }
    assert Comment.objects.count() == 1
    comment = Comment.objects.get(id=comment_id)
    assert comment.ig_id == comment_ig_id
    assert comment.ig_text == comment_ig_text
    assert comment.post.id == post.id


@pytest.mark.django_db
def test_error_comment_post_not_found(
    api_client, requests_mock, api_url, access_token
):
    """
    Проверяет обработку ошибки, если пост Instagram с указанным `id`
    отсутствует в базе.
    """

    comment_ig_text = "Text"
    error_text = "No Post matches the given query."
    url = reverse("api:posts-comment", kwargs={"pk": 1})
    requests_mock.post(
        f"{api_url}1/comments?message={comment_ig_text}"
        f"&access_token={access_token}",
        json={"detail": error_text},
    )
    assert Post.objects.count() == 0
    response = api_client.post(url, {"ig_text": comment_ig_text})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == error_text
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_error_when_post_not_found_in_instagram(
    api_client, requests_mock, api_url, access_token, post, comment_post_url
):
    """
    Проверяет обработку ошибки, если указанный пост существует в базе, но его
    уже нет в Instagram.
    """

    comment_ig_text = "Text"
    requests_mock.post(
        f"{api_url}{post.ig_id}/comments?message={comment_ig_text}"
        f"&access_token={access_token}",
        json={
            "error": {
                "message": "Unsupported post request...",
                "type": "IGApiException",
                "code": 100,
                "error_subcode": 33,
                "fbtrace_id": "ABCDEFGHIJKLMNOP",
            }
        },
    )
    assert Comment.objects.count() == 0
    response = api_client.post(comment_post_url, {"ig_text": comment_ig_text})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "Пост не найден"
    assert Comment.objects.count() == 0
