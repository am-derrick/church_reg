"""
app configuration for the custom_admin app
"""

from django.apps import AppConfig


class CustomAdminConfig(AppConfig):
    """
    Custom admin configuration
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "custom_admin"
