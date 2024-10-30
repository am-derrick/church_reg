"""
module for signals to log changes and deletion
"""

from threading import local

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict

from members.models import Registration
from .models import AuditLog


def log_change(instance, action, user=None, changes=None):
    """Helper function to create audit log entries"""

    # Get request data from thread local storage if available
    try:
        _thread_locals = local()
        request = getattr(_thread_locals, "request", None)
    except AttributeError:
        request = None

    audit_data = {}
    if request:
        audit_data = getattr(request, "audit_data", {})

    AuditLog.objects.create(
        user=user,
        action=action,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=str(instance.pk),
        changes=changes,
        ip_address=audit_data.get("ip_address"),
        user_agent=audit_data.get("user_agent"),
    )


@receiver(post_save, sender=Registration)
def log_registration_change(instance, created):
    """Log changes to the Registration model"""
    action = "CREATE" if created else "UPDATE"

    # For updates, get the changes
    changes = None
    if not created:
        try:
            old_instance = Registration.objects.get(pk=instance.pk)
            old_data = model_to_dict(old_instance)
            new_data = model_to_dict(instance)
            changes = {
                field: {"old": old_data[field], "new": new_data[field]}
                for field in new_data
                if old_data[field] != new_data[field]
            }
        except Registration.DoesNotExist:
            pass

    log_change(instance, action, changes=changes)


@receiver(post_delete, sender=Registration)
def log_registration_deletion(instance):
    """Log deletion of Registration records"""
    log_change(instance, "DELETE")
