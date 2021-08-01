from django import forms
from .models import *

import re
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class roomForm(forms.ModelForm):
    class Meta:
        model = roomModel
        fields = ['room_name']
        widgets = {
            'room_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_room_name(self):
        room_name = self.cleaned_data['room_name']
        if ' ' in room_name:
            raise ValidationError('Space in your room name.') 
        return room_name

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=16, label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=16, label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))