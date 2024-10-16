from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registration_view, name='register'),
    path('welcome/<str:first_name>/', views.welcome_view, name='welcome')
]