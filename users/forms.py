from django import forms
from .models import CustomUser


class EmailRequestForm(forms.Form):
    email = forms.EmailField()


class CodeVerificationForm(forms.Form):
    code = forms.CharField(max_length=6)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["bio", "profile_image"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "maxlength": 500}),
        }