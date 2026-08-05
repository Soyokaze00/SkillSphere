from django.contrib import admin

from .models import (
    Comment,
    Project,
    ProjectFile,
    ProjectInvitation,
    ProjectLike,
    ProjectMember,
)


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 0
    autocomplete_fields = ("user",)


class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 0
    autocomplete_fields = ("uploaded_by",)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "visibility",
        "status",
        "views_count",
        "download_count",
        "like_count_display",
        "member_count_display",
        "created_at",
    )
    list_filter = (
        "visibility",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "description",
        "tags",
        "owner__username",
        "owner__email",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "like_count_display",
        "member_count_display",
        "tag_list_display",
    )
    autocomplete_fields = ("owner",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    inlines = [ProjectMemberInline, ProjectFileInline, CommentInline]

    fieldsets = (
        (
            "Project Info",
            {
                "fields": (
                    "title",
                    "description",
                    "owner",
                )
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "visibility",
                    "status",
                    "tags",
                )
            },
        ),
        (
            "Stats",
            {
                "fields": (
                    "views_count",
                    "download_count",
                    "like_count_display",
                    "member_count_display",
                    "tag_list_display",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="Likes")
    def like_count_display(self, obj):
        return obj.like_count

    @admin.display(description="Members")
    def member_count_display(self, obj):
        return obj.member_count

    @admin.display(description="Tag List")
    def tag_list_display(self, obj):
        return ", ".join(obj.tag_list) if obj.tag_list else "-"


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "user",
        "joined_at",
    )
    list_filter = ("joined_at",)
    search_fields = (
        "project__title",
        "user__username",
        "user__email",
    )
    readonly_fields = ("joined_at",)
    autocomplete_fields = (
        "project",
        "user",
    )
    ordering = ("-joined_at",)


@admin.register(ProjectInvitation)
class ProjectInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "email",
        "invited_by",
        "status",
        "created_at",
        "responded_at",
        "is_pending",
    )
    list_filter = (
        "status",
        "created_at",
        "responded_at",
    )
    search_fields = (
        "project__title",
        "email",
        "invited_by__username",
        "invited_by__email",
        "token",
    )
    readonly_fields = (
        "token",
        "created_at",
        "responded_at",
        "is_pending",
    )
    autocomplete_fields = (
        "project",
        "invited_by",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Invitation Info",
            {
                "fields": (
                    "project",
                    "email",
                    "invited_by",
                    "token",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "is_pending",
                    "created_at",
                    "responded_at",
                )
            },
        ),
    )

    @admin.action(description="Mark selected invitations as accepted")
    def mark_as_accepted(self, request, queryset):
        for invite in queryset:
            invite.mark_accepted()

    @admin.action(description="Mark selected invitations as declined")
    def mark_as_declined(self, request, queryset):
        for invite in queryset:
            invite.mark_declined()

    actions = ("mark_as_accepted", "mark_as_declined")


@admin.register(ProjectLike)
class ProjectLikeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "user",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "project__title",
        "user__username",
        "user__email",
    )
    readonly_fields = ("created_at",)
    autocomplete_fields = (
        "project",
        "user",
    )
    ordering = ("-created_at",)


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "filename",
        "display_path",
        "uploaded_by",
        "uploaded_at",
    )
    list_filter = ("uploaded_at",)
    search_fields = (
        "project__title",
        "file",
        "relative_path",
        "uploaded_by__username",
        "uploaded_by__email",
    )
    readonly_fields = (
        "filename",
        "display_path",
        "uploaded_at",
    )
    autocomplete_fields = (
        "project",
        "uploaded_by",
    )
    ordering = ("-uploaded_at",)

    fieldsets = (
        (
            "File Info",
            {
                "fields": (
                    "project",
                    "file",
                    "relative_path",
                    "filename",
                    "display_path",
                    "uploaded_by",
                    "uploaded_at",
                )
            },
        ),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "user",
        "short_text",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "project__title",
        "user__username",
        "user__email",
        "text",
    )
    readonly_fields = ("created_at",)
    autocomplete_fields = (
        "project",
        "user",
    )
    ordering = ("-created_at",)

    @admin.display(description="Comment")
    def short_text(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
