from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.models import User


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("This email already exists")
        return self.cleaned_data['email']
