"""
url patterns for custom_admin app
"""

from django.urls import path
from . import views
from . import export
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("users/", views.user_list, name="user_list"),
    path("users/create/", views.user_create, name="user_create"),
    path("users/<int:user_id>/edit/", views.user_edit, name="user_edit"),
    path(
        "users/<int:user_id>/deactivate/", views.user_deactivate, name="user_deactivate"
    ),
    path(
        "export-registration/",
        export.export_registrations_csv,
        name="export_registrations_csv",
    ),
    path(
        "export/service-attendance/",
        export.export_service_attendance_csv,
        name="export_service_attendance",
    ),
    path(
        "registration/<int:registration_id>/",
        views.registration_detail,
        name="registration_detail",
    ),
    path(
        "registration/<int:registration_id>/delete",
        views.delete_registration,
        name="delete_registration",
    ),
    path("analytics/", views.attendance_analytics, name="attendance_analytics"),
    path("audit-logs/", views.audit_log_view, name="audit_logs"),
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
