from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["type", "subject", "message", "rating"]
        widgets = {
            "type": forms.HiddenInput(),
            "rating": forms.HiddenInput(),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating") or 0
        if rating < 0 or rating > 5:
            raise forms.ValidationError("Rating must be between 0 and 5.")
        return rating