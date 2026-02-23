from datetime import datetime, timezone

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from api.models import Post


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def access_token():
    return "TestAccessToken11223344556677889900"


@pytest.fixture(autouse=True)
def set_env(settings, access_token):
    settings.INSTAGRAM_API_ACCESS_TOKEN = access_token


@pytest.fixture
def api_url():
    return "https://graph.instagram.com/v25.0/"


@pytest.fixture
def post():
    return Post.objects.create(
        ig_id="98765432109876543",
        ig_media_type="IMAGE",
        ig_media_url="https://cdninstagram.com/post.jpg",
        ig_timestamp=datetime.now(timezone.utc),
        ig_caption="Text.",
        ig_comments_count=0,
        ig_like_count=1,
    )


@pytest.fixture
def comment_post_url(post):
    return reverse("api:posts-comment", kwargs={"pk": post.pk})
