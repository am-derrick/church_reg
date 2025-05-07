"""
url patterns for the ``admin``, ``events``, ``members`` and ``custom_admin``
apps of the ``church_registration`` project
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("members/", include("members.urls")),
    path("events/", include("events.urls")),
    path("custom_admin/", include("custom_admin.urls")),
]
