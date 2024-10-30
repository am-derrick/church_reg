"""
contains url patterns for the members app
"""

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registration_view, name='register'),
    path('register/confirm/', views.registration_confirm, name='registration_confirm'),
    path('register/submit/', views.registration_submit, name='registration_submit'),
    path('welcome/<str:first_name>/', views.welcome_view, name='welcome'),
]
