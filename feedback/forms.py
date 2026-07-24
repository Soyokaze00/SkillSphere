from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = (
            "subject",
            "category",
            "message",
        )

    def clean_subject(self):
        subject = self.cleaned_data["subject"].strip()

        if len(subject) < 5:
            raise forms.ValidationError(
                "Subject must contain at least 5 characters."
            )

        return subject

    def clean_message(self):
        message = self.cleaned_data["message"].strip()

        if len(message) < 10:
            raise forms.ValidationError(
                "Message must contain at least 10 characters."
            )

        return message