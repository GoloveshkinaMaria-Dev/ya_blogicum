# Django
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

# local
from blog.constants import TITLE_MAX_LENGTH


User = get_user_model()


class Category(models.Model):
    title = models.CharField(_("Заголовок"), max_length=TITLE_MAX_LENGTH)
    is_published = models.BooleanField(_("Опубликовано"), default=True)
    slug = models.SlugField(
        _("Идентификатор"),
        unique=True,
        help_text=_(
            "Идентификатор страницы для URL; "
            "разрешены символы латиницы, цифры, дефис и подчёркивание."
        ),
    )
    description = models.TextField(_("Описание"), blank=True)

    class Meta:
        verbose_name = _("категория")
        verbose_name_plural = _("категории")

    def __str__(self):
        return self.title


class Location(models.Model):
    name = models.CharField(_("Название места"), max_length=TITLE_MAX_LENGTH)

    class Meta:
        verbose_name = _("местоположение")
        verbose_name_plural = _("местоположения")

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(_("Заголовок"), max_length=TITLE_MAX_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(_("Текст"))
    pub_date = models.DateTimeField(_("Дата публикации"))
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("Автор публикации"),
    )
    image = models.ImageField(
        _("Изображение"), upload_to="posts/", blank=True, null=True
    )
    is_published = models.BooleanField(_("Опубликовано"), default=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name=_("Категория"),
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name=_("Местоположение"),
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = _("публикация")
        verbose_name_plural = _("публикации")

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Публикация"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Автор"),
    )
    text = models.TextField(_("Комментарий"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("комментарий")
        verbose_name_plural = _("комментарии")

    def __str__(self):
        return f"Комментарий от {self.author} к {self.post}"
