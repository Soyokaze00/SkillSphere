from django.contrib import admin
from django.utils import timezone

from notifications.models import Notification

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "user",
        "type",
        "status",
        "admin_reaction",
        "rating",
        "created_at",
    )
    list_filter = (
        "type",
        "status",
        "admin_reaction",
    )
    search_fields = (
        "subject",
        "message",
        "user__username",
    )
    list_editable = (
        "status",
        "admin_reaction",
    )

    readonly_fields = (
        "user",
        "type",
        "subject",
        "message",
        "rating",
        "created_at",
        "admin_responded_at",
    )

    fieldsets = (
        (
            "Feedback",
            {
                "fields": (
                    "user",
                    "type",
                    "subject",
                    "message",
                    "rating",
                    "created_at",
                ),
            },
        ),
        (
            "Team Response",
            {
                "fields": (
                    "status",
                    "admin_reaction",
                    "admin_response",
                    "admin_responded_at",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        response_changed = (
            "admin_response" in form.changed_data
            or "admin_reaction" in form.changed_data
        )

        cleaned_response = (
            obj.admin_response or ""
        ).strip()

        has_response = bool(
            cleaned_response or obj.admin_reaction
        )

        responded_now = (
            response_changed and has_response
        )

        if responded_now:
            obj.admin_responded_at = timezone.now()

        super().save_model(
            request,
            obj,
            form,
            change,
        )

        if responded_now and obj.user_id:
            Notification.objects.create(
                user=obj.user,
                type="feedback",
                title="Your feedback got a response",
                message=(
                    cleaned_response
                    or (
                        f"The team reacted "
                        f"{obj.admin_reaction} "
                        f"to your feedback."
                    )
                ),
                link="/feedback/",
            )
