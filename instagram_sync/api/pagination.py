from rest_framework.pagination import CursorPagination


class PostCursorPagination(CursorPagination):
    """Курсорная пагинация для постов Instagram."""

    page_size = 3
    ordering = "-ig_timestamp"
