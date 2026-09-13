"""
Вспомогательные функции приложения blog.

Содержит функции для получения опубликованных публикаций
и общей логики, используемой в представлениях.
"""

from django.utils import timezone

from .models import Post


def get_published_posts(queryset=None):
    """Возвращает опубликованные посты с проверкой категории."""
    if queryset is None:
        queryset = Post.objects.all()

    now = timezone.now()
    return queryset.filter(
        is_published=True, pub_date__lte=now, category__is_published=True
    ).exclude(
        category__slug=""
    )
