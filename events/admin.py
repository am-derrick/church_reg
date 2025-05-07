"""
module for members admin app
"""

from django.contrib import admin
from .models import Registration

admin.site.register(Registration)
