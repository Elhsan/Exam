from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             help_text="We never share your email with anyone else.",
                             widget=forms.EmailInput(attrs={'class': 'email-field'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'username-field'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password-field'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password-confirm-field'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
