from django.db import models
from django.utils import timezone

class Registration(models.Model):
    """Registration form input fields model"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')])
    phone_number = models.CharField(max_length=12, unique=True)
    residence = models.CharField(max_length=255)
    is_student = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    institution_location = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    is_first_time = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    consent = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"