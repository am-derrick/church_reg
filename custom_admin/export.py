"""
module contains functions for exporting data to csv files
"""

import csv
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse
from django.utils.timezone import make_aware
from members.models import Registration
from .utils import permission_required, is_admin


@permission_required(is_admin)
def export_registrations_csv(request):
    """Export registrations to CSV with filter options"""
    order_by = request.GET.get("order_by", "-created_at")
    search_query = request.GET.get("search", "")
    date_range = request.GET.get("date_range", "")
    status_filter = request.GET.get("status", "")
    selected_columns = request.GET.getlist("columns", [])  # For column selection

    registrations = Registration.objects.all()

    if search_query:
        registrations = registrations.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(phone_number__icontains=search_query)
            | Q(residence__icontains=search_query)
            | Q(institution_name__icontains=search_query)
            | Q(occupation__icontains=search_query)
        )

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
            pass

    if status_filter:
        if status_filter == "student":
            registrations = registrations.filter(is_student="Yes")
        elif status_filter == "first_time":
            registrations = registrations.filter(is_first_time="Yes")
        elif status_filter == "consent":
            registrations = registrations.filter(consent="Yes")

    registrations = registrations.order_by(order_by)

    # Available columns and their display names
    all_columns = {
        "first_name": "First Name",
        "last_name": "Last Name",
        "gender": "Gender",
        "phone_number": "Phone Number",
        "residence": "Residence",
        "is_student": "Student",
        "institution_name": "Institution Name",
        "institution_location": "Institution Location",
        "occupation": "Occupation",
        "is_first_time": "First Time",
        "consent": "Consent",
        "created_at": "Created At",
        "last_updated": "Last Updated",
    }

    # Export selected columns or all columns if none is slesscted
    columns_to_export = selected_columns if selected_columns else all_columns.keys()

    # HttpResponseobject created with CSV header
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"registrations_export_(timestamp).csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)

    # Write header row for selected columns
    header_row = [all_columns[col] for col in columns_to_export]
    writer.writerow(header_row)

    # Write data rows
    for registration in registrations:
        row = []
        for column in columns_to_export:
            value = getattr(registration, column)
            if isinstance(value, datetime):
                value = value.strftime("%d-%m-%Y %H:%M")
            row.append(str(value))
        writer.writerow(row)

    return response
