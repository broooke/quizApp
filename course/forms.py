from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['name']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = '__all__'

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
