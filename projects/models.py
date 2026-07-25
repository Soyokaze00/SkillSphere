import secrets

from django.db import models
from django.conf import settings
from django.utils import timezone
import secrets


# Create your models here.


def generate_invitation_token():
    return secrets.token_urlsafe(32)

class Project(models.Model):

    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

    VISIBILITY_CHOICES = [
        (PUBLIC, "Public"),
        (PRIVATE, "Private"),
    ]

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField()

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects"
    )

    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default="PUBLIC"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated tags, e.g. 'django,react,api'"
    )

    views_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]  

    
    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        """Returns the comma-separated tags string as a clean list."""
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(",") if t.strip()]

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def member_count(self):
        """
        Total members including the project owner.
        ProjectMember only stores collaborators, so we add the owner.
        """
        return self.memberships.count() + 1

    def is_liked_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()


    
class ProjectMember(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        unique_together = ("project", "user")


class ProjectInvitation(models.Model):
    """
    An outstanding invite to collaborate on a project, sent to an email
    address. Nothing in ProjectMember gets created until the recipient
    clicks the accept link -- see views.accept_invite.
    """

    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (DECLINED, "Declined"),
        (CANCELLED, "Cancelled"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="invitations"
    )

    email = models.EmailField()

    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_invitations"
    )

    token = models.CharField(
        max_length=64,
        unique=True,
        default=generate_invitation_token,
        editable=False,
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Invite to {self.email} for {self.project.title} ({self.status})"

    @property
    def is_pending(self):
        return self.status == self.PENDING

    def mark_accepted(self):
        self.status = self.ACCEPTED
        self.responded_at = timezone.now()
        self.save(update_fields=["status", "responded_at"])

    def mark_declined(self):
        self.status = self.DECLINED
        self.responded_at = timezone.now()
        self.save(update_fields=["status", "responded_at"])


class ProjectLike(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user.username} likes {self.project.title}"




class ProjectFile(models.Model):
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name="files"
    )
    file = models.FileField(upload_to="project_files/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="uploaded_project_files"
    )

    relative_path = models.CharField(max_length=500, blank=True)

    @property
    def filename(self):
        import os
        return os.path.basename(self.file.name)

    @property
    def display_path(self):
        """What to show in the UI: the original folder path if we have
        one, otherwise just the stored filename."""
        return self.relative_path or self.filename

    def __str__(self):
        return f"{self.project.title} - {self.file.name}"



class Comment(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} on {self.project.title}"