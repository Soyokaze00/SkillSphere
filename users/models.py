from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    avatar_seed = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Follow(models.Model):
    """
    follower -> following : "follower" follows "following".
    user.following.all() -> who this user follows
    (user is the follower).
    user.followers.all() -> who follows this user
    (user is being followed).
    """

    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
        constraints = [
            models.CheckConstraint(
                check=~models.Q(follower=models.F("following")),
                name="users_follow_cant_follow_self",
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"
