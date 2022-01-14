from django import forms
from django.contrib.auth.models import User

class CreateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    email = forms.CharField()

class Meta:
    model= User
    fields =('username','password','email')