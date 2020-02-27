from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.models import User

from .models import Article


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


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'