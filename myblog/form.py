from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    # using form model to create an email field
    email = forms.EmailField()

    class Meta:
        # This belong to user model
        model = User
        fields = ['username','email','password1','password2']