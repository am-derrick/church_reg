from django.urls import path
from . import views
from . import export

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:user_id>/deactivate/', views.user_deactivate, name='user_deactivate'),
    path('export-registration/', export.export_registrations_csv, name='export_registrations_csv')
]