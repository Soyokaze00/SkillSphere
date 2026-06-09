from django import forms


class EmailRequestForm(forms.Form):
    email = forms.EmailField()


class CodeVerificationForm(forms.Form):
    code = forms.CharField(max_length=6)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)