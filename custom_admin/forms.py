"""
module for creating and changing user form
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """class for creating user form"""
    class Meta(UserCreationForm.Meta):
        """Meta details for creating user"""
        model = User
        fields = ('username', 'email', 'role')

class CustomUserChangeForm(UserChangeForm):
    """class for changing user form"""
    password = None

    class Meta:
        """Meta details for changing user"""
        model = User
        fields = ('username', 'email', 'role', 'is_active')
