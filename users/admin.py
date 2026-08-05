from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, EmailVerification, Follow


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
        "groups",
    )
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
    ordering = ("id",)

    fieldsets = list(UserAdmin.fieldsets or []) + [
        (
            "Extra Info",
            {
                "fields": (
                    "bio",
                    "profile_image",
                    "avatar_seed",
                )
            },
        ),
    ]

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Extra Info",
            {
                "fields": (
                    "email",
                    "bio",
                    "profile_image",
                    "avatar_seed",
                )
            },
        ),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "code",
        "is_verified",
        "created_at",
    )
    list_filter = (
        "is_verified",
        "created_at",
    )
    search_fields = (
        "email",
        "code",
    )
    ordering = ("-created_at",)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "follower",
        "following",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "follower__username",
        "follower__email",
        "following__username",
        "following__email",
    )
    ordering = ("-created_at",)
