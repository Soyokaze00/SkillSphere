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
        fields = ["username", "bio", "profile_image", "avatar_seed"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "w-full mt-2 px-4 py-3 rounded-xl border border-gray-300 bg-gray-50 outline-none focus:ring-2 focus:ring-indigo-500",
            }),
            "bio": forms.Textarea(attrs={
                "rows": 4,
                "maxlength": 500,
                "class": "w-full mt-2 px-4 py-3 rounded-xl border border-gray-300 bg-gray-50 outline-none resize-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Tell people a bit about yourself...",
            }),
            "profile_image": forms.FileInput(attrs={
                "class": "text-sm text-gray-600 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-indigo-50 file:text-indigo-600 file:text-sm file:font-semibold hover:file:bg-indigo-100 file:cursor-pointer",
            }),
            "avatar_seed": forms.HiddenInput(),
        }