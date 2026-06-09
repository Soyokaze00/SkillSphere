from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("bio", "profile_image")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Info", {
            "classes": ("wide",),
            "fields": ("bio", "profile_image"),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
