from rest_framework.pagination import CursorPagination


class PostCursorPagination(CursorPagination):
    """Постраничная навигация для постов с использованием курсора."""

    page_size = 3
    ordering = "-ig_timestamp"
