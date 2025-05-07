"""
contains url patterns for the members app
"""

from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.events_view, name="register"),
    path("events/confirm/", views.events_confirm, name="events_confirm"),
    path("events/submit/", views.events_submit, name="events_submit"),
    path("welcome/<str:first_name>/", views.welcome_view, name="welcome"),
]
