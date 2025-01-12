"""
module containing views for the custom_admin app
"""

from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from members.models import Registration
from members.models import ServiceAttendance
from .utils import get_page_range
from .utils import permission_required, is_super_admin, is_admin, get_client_ip
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import AuditLog

User = get_user_model()


def login_view(request):
    """login view"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Log successful login
            AuditLog.objects.create(
                user=user,
                action="LOGIN",
                ip_address=get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )
            return redirect("admin_dashboard")
        messages.error(request, "Invalid username or password")
    return render(request, "custom_admin/login.html")


@login_required
def logout_view(request):
    """logout view"""
    logout(request)
    return redirect("login")


class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view"""

    template_name = "custom_admin/password_reset_form.html"
    email_template_name = "custom_admin/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        # Log the password reset request
        AuditLog.objects.create(
            user=None,  # Since user is not authenticated
            action="PASSWORD_RESET_REQUEST",
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get("HTTP_USER_AGENT", ""),
        )
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Custom password reset done view"""

    template_name = "custom_admin/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Custom password reset confirm view"""

    template_name = "custom_admin/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the successful password reset
        AuditLog.objects.create(
            user=self.user,
            action="PASSWORD_RESET_COMPLETE",
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get("HTTP_USER_AGENT", ""),
        )
        return response


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Custom password reset complete view"""

    template_name = "custom_admin/password_reset_complete.html"


@login_required
def admin_dashboard(request):
    """view for the admin dashboard with pagination"""
    order_by = request.GET.get("order_by", "-created_at")
    search_query = request.GET.get("search", "")
    date_range = request.GET.get("date_range", "")
    status_filter = request.GET.get("status", "")

    registrations = Registration.objects.all()

    # Search filter
    if search_query:
        registrations = registrations.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(phone_number__icontains=search_query)
            | Q(residence__icontains=search_query)
            | Q(institution_name__icontains=search_query)
            | Q(occupation__icontains=search_query)
        )

    # Date range filter
    if date_range:
        try:
            start_date, end_date = date_range.split(" to ")
            start_date = datetime.strptime(start_date, "%d-%m-%Y")
            end_date = datetime.strptime(end_date, "%d-%m-%Y")
            start_date = make_aware(start_date)
            end_date = end_date.replace(hour=23, minute=59, second=59)
            registrations = registrations.filter(
                created_at__range=[start_date, end_date]
            )
        except (ValueError, AttributeError):
            messages.error(
                request, "Invalid date range format. Please use DD-MM-YYYY format"
            )

    # Status filter
    if status_filter:
        if status_filter == "student":
            registrations = registrations.filter(is_student="Yes")
        elif status_filter == "first_time":
            registrations = registrations.filter(is_first_time="Yes")
        elif status_filter == "consent":
            registrations = registrations.filter(consent="Yes")

    registrations = registrations.order_by(order_by)
    paginator = Paginator(registrations, 25)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    page_range = get_page_range(paginator, page_obj)

    context = {
        "registrations": page_obj,
        "order_by": order_by,
        "page_range": page_range,
        "search_query": search_query,
        "date_range": date_range,
        "status_filter": status_filter,
        "is_admin": is_admin(request.user),
        "is_super_admin": is_super_admin(request.user),
    }

    return render(request, "custom_admin/admin_dashboard.html", context)


@login_required
def user_list(request):
    """displays list for all users(admins)"""
    users = User.objects.all().order_by("-date_joined")
    return render(request, "custom_admin/user_list.html", {"users": users})


@login_required
@permission_required(is_admin)
def user_create(request):
    """super user creates admins"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect("user_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "custom_admin/user_form.html", {"form": form})


@login_required
@permission_required(is_admin)
def user_edit(request, user_id):
    """super user edits users"""
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updates successfully.")
            return redirect("user_list")
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, "custom_admin/user_form.html", {"form": form})


@login_required
@permission_required(is_super_admin)
def user_deactivate(request, user_id):
    """super user deactivates other users"""
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
        return redirect("user_list")
    user.is_active = False
    user.save()
    messages.success(request, "User deactivated succesfully.")
    return redirect("user_list")


@login_required
def registration_detail(request, registration_id):
    """View for differnent admin registraion details"""
    registration = get_object_or_404(Registration, id=registration_id)

    # If user  is regular user, hide senstitive information
    if not is_admin(request.user):
        registration.phone_number = "**********"
        registration.residence = "Hidden"

    context = {
        "registration": registration,
        "is_admin": is_admin(request.user),
        "is_super_admin": is_super_admin(request.user),
    }

    return render(request, "custom_admin/registration_detail.html", context)


@login_required
@permission_required(is_super_admin)
def delete_registration(request, registration_id):
    """Delete registration entry, available for only super admin"""
    registration = get_object_or_404(Registration, id=registration_id)
    if request.method == "POST":
        registration.delete()
        messages.success(request, "Registration entry deleted successfully.")
        return redirect("admin_dashboard")
    return HttpResponseForbidden()


@login_required
def attendance_analytics(request):
    """View for displaying attendance analytics"""
    try:
        daily_attendance = (
            ServiceAttendance.objects.annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(
                total_attendance=Count("id"),
                new_registrations=Count("id", filter=Q(attendance_type="NEW")),
                updates=Count("id", filter=Q(attendance_type="UPDATE")),
                confirmations=Count("id", filter=Q(attendance_type="CONFIRM")),
            )
            .order_by("-date")
        )

        attendance_list = list(daily_attendance)

        context = {
            "daily_attendance": attendance_list,
        }

        return render(request, "custom_admin/analytics.html", context)
    except Exception as e:
        context = {
            "daily_attendance": [],
            "error_message": f"An error occurred while fetching attendance data: {str(e)}",
        }
        return render(request, "custom_admin/analytics.html", context)


@login_required
@permission_required(is_super_admin)
def audit_log_view(request):
    """View for displaying audit logs with filters"""
    logs = AuditLog.objects.select_related("user", "content_type").all()

    # Filters
    user_filter = request.GET.get("user")
    action_filter = request.GET.get("action")
    date_range = request.GET.get("date_range")

    if user_filter:
        logs = logs.filter(user_id=user_filter)
    if action_filter:
        logs = logs.filter(action=action_filter)
    if date_range:
        try:
            start_date, end_date = date_range.split(" to ")
            start_date = datetime.strptime(start_date, "%d-%m-%Y")
            end_date = datetime.strptime(end_date, "%d-%m-%Y")
            start_date = make_aware(start_date)
            end_date = end_date.replace(hour=23, minute=59, second=59)
            logs = logs.filter(timestamp__range=[start_date, end_date])
        except (ValueError, AttributeError):
            messages.error(request, "Invalid date range format")

    # Pagination
    paginator = Paginator(logs, 50)
    page = request.GET.get("page")
    logs = paginator.get_page(page)

    context = {
        "logs": logs,
        "users": User.objects.all(),
        "actions": AuditLog.ACTION_TYPES,
    }

    return render(request, "custom_admin/audit_logs.html", context)
