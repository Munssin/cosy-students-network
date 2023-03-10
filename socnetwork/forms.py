from django import forms
from django.forms import ModelForm
from .models import UsersProfile

class UsersProfileForm(ModelForm):
     class Meta:
        model = UsersProfile
        fields = ('about', 'university', 'avatar')