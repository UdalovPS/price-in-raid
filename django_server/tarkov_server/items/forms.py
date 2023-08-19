from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses is alredy exists')
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class LanguageForm(forms.Form):
    CHOICES = (
        ('eng', u"eng"),
        ('rus', u"rus")
    )
    language = forms.ChoiceField(choices=CHOICES)


class DropForm(forms.Form):
    email = forms.EmailField()
