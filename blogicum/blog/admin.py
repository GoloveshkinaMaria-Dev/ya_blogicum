from django.contrib import admin

from blog.models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административная конфигурация модели Category."""

    list_display = ("title", "slug", "description")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Административная конфигурация модели Location."""

    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Административная конфигурация модели Post."""

    list_display = (
        "title",
        "pub_date",
        "author",
        "is_published",
        "category",
        "location",
    )
    list_filter = ("is_published", "category", "pub_date", "location")
    search_fields = ("title", "text")
    list_select_related = ("category", "location", "author")
