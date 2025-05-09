"""
contains url patterns for the members app
"""

from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registration_view, name="register"),
    path("register/confirm/", views.registration_confirm, name="registration_confirm"),
    path("register/submit/", views.registration_submit, name="registration_submit"),
    path("welcome/<str:first_name>/", views.welcome_view, name="welcome"),
    path("events/", views.events_register_view, name="events"),
    path("events/submit/", views.events_submit, name="events_submit"),
    path("events/confirm/", views.events_confirm, name="events_confirm"),
]
