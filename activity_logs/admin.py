from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "method",
        "path",
        "status_code",
        "ip_address",
        "created_at",
    )
    list_filter = (
        "action",
        "method",
        "status_code",
        "created_at",
    )
    search_fields = (
        "user__username",
        "description",
        "path",
        "ip_address",
    )
    readonly_fields = (
        "user",
        "action",
        "description",
        "path",
        "method",
        "status_code",
        "ip_address",
        "created_at",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
