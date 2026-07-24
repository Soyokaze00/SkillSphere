from django.conf import settings
from django.db import models


class Feedback(models.Model):
    class Category(models.TextChoices):
        SUGGESTION = "SUGGESTION", "Suggestion"
        BUG_REPORT = "BUG_REPORT", "Bug Report"
        COMPLAINT = "COMPLAINT", "Complaint"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        REVIEWING = "REVIEWING", "Reviewing"
        RESOLVED = "RESOLVED", "Resolved"
        REJECTED = "REJECTED", "Rejected"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )

    subject = models.CharField(
        max_length=200,
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    admin_response = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.subject} - {self.user.username}"