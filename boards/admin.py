from django.contrib import admin
from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "content",
        "created_at",
    )
    list_display_links = (
        "id",
        "title",
    )
    search_fields = (
        "title",
        "content",
    )
    list_filter = (
        "title",
        "created_at",
    )

    search_fields = (
        # "title",
        "content",
    )
