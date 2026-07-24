from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "user",
        "category",
        "status",
        "created_at",
    )

    list_filter = (
        "category",
        "status",
        "created_at",
    )

    search_fields = (
        "subject",
        "message",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "user",
        "subject",
        "category",
        "message",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )