from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """class for creating user form"""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')

class CustomUserChangeForm(UserChangeForm):
    """class for changing user form"""
    password = None

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'is_active')