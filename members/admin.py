"""This file is used to register the model in the admin panel"""
from django.contrib import admin
from .models import Registration
# Register your models here
admin.site.register(Registration)
