from .models import *

from django import forms

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'birth_date', 'interests']

        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }