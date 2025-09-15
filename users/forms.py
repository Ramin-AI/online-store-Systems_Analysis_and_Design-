from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserSignUpForm(UserCreationForm):
    """
    Form for user registration with username and password fields.
    """
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    """
    Form for user login with username and password fields.
    """
    class Meta:
        model = User
        fields = ('username', 'password')