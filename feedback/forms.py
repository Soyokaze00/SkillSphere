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

        widgets = {
            "subject": forms.TextInput(
                attrs={
                    "class": (
                        "mt-2 block w-full rounded-xl border "
                        "border-slate-300 bg-white px-4 py-3 "
                        "text-slate-900 placeholder:text-slate-400 "
                        "outline-none transition "
                        "focus:border-violet-500 focus:ring-2 "
                        "focus:ring-violet-200 "
                        "dark:border-slate-600 dark:bg-slate-800 "
                        "dark:text-white"
                    ),
                    "placeholder": "Enter a short subject",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": (
                        "mt-2 block w-full rounded-xl border "
                        "border-slate-300 bg-white px-4 py-3 "
                        "text-slate-900 outline-none transition "
                        "focus:border-violet-500 focus:ring-2 "
                        "focus:ring-violet-200 "
                        "dark:border-slate-600 dark:bg-slate-800 "
                        "dark:text-white"
                    ),
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": (
                        "mt-2 block min-h-36 w-full resize-y "
                        "rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-slate-900 "
                        "placeholder:text-slate-400 outline-none "
                        "transition focus:border-violet-500 "
                        "focus:ring-2 focus:ring-violet-200 "
                        "dark:border-slate-600 dark:bg-slate-800 "
                        "dark:text-white"
                    ),
                    "placeholder": "Describe your suggestion or problem",
                    "rows": 6,
                }
            ),
        }

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