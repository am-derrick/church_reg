from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from members.models import Registration

@login_required
def admin_dashboard(request):
    """view for the admin dashboard"""
    registrations = Registration.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard.html', {'registrations': registrations})
