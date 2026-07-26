from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Project, ProjectFile

User = get_user_model()


class MultipleFileInput(forms.ClearableFileInput):
    """
    Django 5's FileInput/ClearableFileInput refuse a bare multiple=True
    attr (they raise ValueError). This is the pattern Django's own docs
    recommend: a widget subclass that opts in via allow_multiple_selected.
    """
    allow_multiple_selected = True


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

        fields = [
            "title",
            "description",
            "status",
            "visibility",
            "tags",
        ]

class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ['file']
        widgets = {
            # See MultipleFileInput above for why this isn't a plain
            # ClearableFileInput(attrs={'multiple': True}).
            'file': MultipleFileInput(),
        }


class InviteMemberForm(forms.Form):
    """
    Owner-only form for inviting a collaborator. Accepts either a
    username (resolved to that account's email) or a raw email address
    (which may or may not belong to an existing account -- the invite
    still gets sent either way).
    """

    identifier = forms.CharField(
        max_length=254,
        label="Username or email",
    )

    def clean_identifier(self):
        raw = self.cleaned_data["identifier"].strip()
        matched_user = None

        if "@" in raw:
            try:
                validate_email(raw)
            except DjangoValidationError:
                raise forms.ValidationError("Enter a valid username or email address.")
            email = raw.lower()
            matched_user = User.objects.filter(email__iexact=email).first()
        else:
            matched_user = User.objects.filter(username__iexact=raw).first()
            if not matched_user:
                raise forms.ValidationError("No user found with that username.")
            if not matched_user.email:
                raise forms.ValidationError(
                    f"{matched_user.username} doesn't have an email on file."
                )
            email = matched_user.email.lower()

        self.matched_user = matched_user
        self.email = email
        return raw