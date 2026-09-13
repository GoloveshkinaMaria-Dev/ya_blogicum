"""Конфигурация приложения blog для проекта Django."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogConfig(AppConfig):
    """Конфигурация приложения blog."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
    verbose_name = _("Блог")
