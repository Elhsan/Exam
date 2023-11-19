from django import forms
from django.contrib.auth.models import User
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'price']