"""
This module contains the models for the members of the church,
including registration details and other relevant data structures.
"""
from django.db import models


class Registration(models.Model):
    """Registration form input fields model"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=[
                              ('Male', 'Male'), ('Female', 'Female')])
    phone_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    residence = models.CharField(max_length=255)
    is_student = models.CharField(
        max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    institution_location = models.CharField(
        max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    is_first_time = models.CharField(
        max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    consent = models.CharField(max_length=3, choices=[
                               ('Yes', 'Yes'), ('No', 'No')])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
