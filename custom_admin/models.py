from django.contrib.auth.models import AbstractUser
from django.db import models

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