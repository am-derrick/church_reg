"""
app configuration for the members app
"""

from django.apps import AppConfig


class MembersConfig(AppConfig):
    """
    Members app configuration
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "members"
