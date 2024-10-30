from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class CustomUser(AbstractUser):
    """Role based admins (users)"""
    SUPER_ADMIN = 'SA'
    MINI_ADMIN = 'MA'
    REGULAR_USER = 'RU'
    ROLE_CHOICES = [
        (SUPER_ADMIN, 'Super Admin'),
        (MINI_ADMIN, 'Mini Admin'),
        (REGULAR_USER, 'Regular User'),
    ]
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=REGULAR_USER)

    def is_super_admin(self):
        return self.role == self.SUPER_ADMIN
    def is_mini_admin(self):
        return self.role == self.MINI_ADMIN
    
User = get_user_model()

class AuditLog(models.Model):
    """class for auditing and tracking logs"""
    ACTION_TYPES = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('EXPORT', 'Export'),
        ('VIEW', 'View'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    # For tracking the specific modified object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=255, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Store the changes
    changes = models.JSONField(null=True, blank=True)

    class Meta:
        """Meta details"""
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['action']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"