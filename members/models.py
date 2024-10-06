from django.db import models

class Registration(models.Model):
    """Registration form input fields model"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    residence = models.CharField(max_length=255)
    is_student = models.BooleanField(default=False)
    is_first_time = models.BooleanField(default=False)
    consent = models.BooleanField(default=False)

    # To-Do: Add field for occupation
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"