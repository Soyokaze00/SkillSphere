from django.conf import settings
from django.db import models


class ActivityLog(models.Model):
    class Action(models.TextChoices):
        LOGIN = "LOGIN", "Login"
        LOGOUT = "LOGOUT", "Logout"
        CREATE_PROJECT = "CREATE_PROJECT", "Create Project"
        UPDATE_PROJECT = "UPDATE_PROJECT", "Update Project"
        DELETE_PROJECT = "DELETE_PROJECT", "Delete Project"
        UPLOAD_FILE = "UPLOAD_FILE", "Upload File"
        DOWNLOAD_FILE = "DOWNLOAD_FILE", "Download File"
        SEND_FEEDBACK = "SEND_FEEDBACK", "Send Feedback"
        OTHER = "OTHER", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
    )

    action = models.CharField(
        max_length=50,
        choices=Action.choices,
        default=Action.OTHER,
    )

    description = models.TextField(blank=True)

    path = models.CharField(
        max_length=500,
        blank=True,
    )

    method = models.CharField(
        max_length=10,
        blank=True,
    )

    status_code = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["action"]),
        ]

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{username} - {self.get_action_display()}"