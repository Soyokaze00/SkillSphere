from django.contrib import admin
from .models import Project, ProjectMember


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "visibility",
        "status",
        "created_at"
    )

    list_filter = (
        "visibility",
        "status"
    )

    search_fields = (
        "title",
        "owner__username"
    )


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "joined_at")
    list_filter = ("project",)
    search_fields = ("user__username", "project__title")