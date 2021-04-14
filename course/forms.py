from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.IntegerField
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']