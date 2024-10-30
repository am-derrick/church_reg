"""
module contains views for the members app
"""

from datetime import date
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.db import IntegrityError
from django.contrib import messages
from .forms import RegistrationForm, NameForm
from .models import Registration, ServiceAttendance


def registration_view(request):
    """Initial registration view: displays name form"""
    if request.method == "POST":
        name_form = NameForm(request.POST)
        if name_form.is_valid():
            first_name = name_form.cleaned_data["first_name"]
            last_name = name_form.cleaned_data["last_name"]

            # Check if name exists in the db
            registration_data = Registration.objects.filter(
                Q(first_name__iexact=first_name) & Q(last_name__iexact=last_name)
            )

            if registration_data.exists():
                # If name exists, render the confirmation page
                return render(
                    request,
                    "members/name_confirmation.html",
                    {"first_name": first_name, "last_name": last_name},
                )
            else:
                # If name doesn't exist, show the full registration form
                form = RegistrationForm(
                    initial={"first_name": first_name, "last_name": last_name}
                )
                return render(request, "members/registration.html", {"form": form})
    name_form = NameForm()

    return render(request, "members/name_form.html", {"form": name_form})


def registration_confirm(request):
    """Confirm existing registration or create new one"""
    if request.method == "POST":
        action = request.POST.get("action")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        # Handle new registration action first
        if action == "new":
            form = RegistrationForm(
                initial={"first_name": first_name, "last_name": last_name}
            )
            return render(request, "members/registration.html", {"form": form})

        try:
            registration = Registration.objects.get(
                Q(first_name__iexact=first_name) & Q(last_name__iexact=last_name)
            )

            # Handle different actions
            if action == "confirm":
                # Check if already registered today only for confirmations
                today = date.today()
                existing_attendance = ServiceAttendance.objects.filter(
                    member=registration, service_date=today
                ).exists()

                if existing_attendance:
                    messages.info(
                        request,
                        f"Welcome back {first_name}! You've already registered for today's service.",
                    )
                    return redirect(
                        reverse("welcome", kwargs={"first_name": first_name})
                    )

                # Create new attendance record for confirmation
                ServiceAttendance.objects.create(
                    member=registration, attendance_type="CONFIRM"
                )
                messages.success(request, "Thank you for confirming your attendance!")
                return redirect(reverse("welcome", kwargs={"first_name": first_name}))

            if action == "update":
                # For updates, always show the form regardless of today's attendance
                form = RegistrationForm(instance=registration)
                return render(
                    request,
                    "members/registration.html",
                    {"form": form, "is_update": True},
                )

        except Registration.DoesNotExist:
            # Handle case where registration doesn't exist
            messages.warning(request, "Registration not found. Please register as new.")
            form = RegistrationForm(
                initial={"first_name": first_name, "last_name": last_name}
            )
            return render(request, "members/registration.html", {"form": form})

    return redirect("register")


def registration_submit(request):
    """Handle registration form submission"""
    if request.method == "POST":
        is_update = request.POST.get("is_update") == "True"

        try:
            if is_update:
                registration = Registration.objects.get(
                    Q(first_name__iexact=request.POST.get("first_name"))
                    & Q(last_name__iexact=request.POST.get("last_name"))
                )
                form = RegistrationForm(request.POST, instance=registration)
            form = RegistrationForm(request.POST)

            if form.is_valid():
                registration = form.save()

                # Check if already registered today
                today = date.today()
                existing_attendance = ServiceAttendance.objects.filter(
                    member=registration, service_date=today
                ).exists()

                if not existing_attendance:
                    ServiceAttendance.objects.create(
                        member=registration,
                        attendance_type="UPDATE" if is_update else "NEW",
                    )

                messages.success(
                    request,
                    (
                        "Registration updated successfully!"
                        if is_update
                        else "Registration successful!"
                    ),
                )
                return redirect(
                    reverse("welcome", kwargs={"first_name": registration.first_name})
                )
            else:
                return render(
                    request,
                    "members/registration.html",
                    {"form": form, "is_update": is_update},
                )

        except IntegrityError:
            messages.info(request, "You've already registered for today's service.")
            return redirect(
                reverse(
                    "welcome", kwargs={"first_name": request.POST.get("first_name")}
                )
            )

    return redirect("register")


def welcome_view(request, first_name):
    """Thank you page view, displayed after registration"""
    return render(
        request,
        "members/welcome.html",
        {"first_name": first_name, "messages": messages.get_messages(request)},
    )
