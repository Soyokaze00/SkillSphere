
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# class Notification(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="notifications"
#     )
#     title = models.CharField(max_length=200)
#     message = models.TextField()
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         ordering = ["-created_at"]

#     def __str__(self):
#         return self.title
    
    
# from django.db import models

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    # TYPE_CHOICES = [
    #     ("download", "Download"),
    #     ("star", "Star"),
    #     ("comment", "Comment"),
    #     ("follow", "Follow"),
    #     ("system", "System"),
    # ]
    TYPE_CHOICES = [
    ("project", "Project"),
    ("comment", "Comment"),
    ("feedback", "Feedback"),
    ("invite", "Invite"),
    ("member", "Member"),
    ("follow", "Follow"),
    ("system", "System"),
    ]

    type = models.CharField(
       max_length=20,
      choices=TYPE_CHOICES,
      default="system"
     )
    link = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return self.title