from django.conf import settings
from django.db import models


class Feedback(models.Model):
    TYPE_SUGGESTION = "suggestion"
    TYPE_BUG = "bug"
    TYPE_FEATURE = "feature"
    TYPE_PRAISE = "praise"

    TYPE_CHOICES = [
        (TYPE_SUGGESTION, "💡 Suggestion"),
        (TYPE_BUG, "🐛 Bug Report"),
        (TYPE_FEATURE, "✨ Feature Request"),
        (TYPE_PRAISE, "🎉 Praise"),
    ]

    STATUS_OPEN = "open"
    STATUS_IN_REVIEW = "in_review"
    STATUS_PLANNED = "planned"
    STATUS_RESOLVED = "resolved"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_IN_REVIEW, "In Review"),
        (STATUS_PLANNED, "Planned"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    REACTION_CHOICES = [
        ("", "No Reaction"),
        ("👍", "👍 Agree"),
        ("❤️", "❤️ Great"),
        ("👀", "👀 We'll Review"),
        ("🎉", "🎉 Done"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="feedbacks",
        null=True,
        blank=True,
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_SUGGESTION)
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=2000)
    rating = models.PositiveSmallIntegerField(default=0)  # 0 to 5
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    admin_reaction = models.CharField(max_length=10, choices=REACTION_CHOICES, blank=True, default="")
    admin_response = models.TextField(max_length=1000, blank=True, default="")
    admin_responded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} ({self.get_type_display()})"
